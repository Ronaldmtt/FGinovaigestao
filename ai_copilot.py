import os
import json
import logging
from datetime import datetime
from openai import OpenAI
from extensions import db
from models import AiChatHistory, User, Project, Task, TodoItem, Meeting, Client, Crm2Lead, FinCostCenter, FinAccount, FinTransaction, FinGoal, FinSupplier, ProjectFile, ProjectApiEndpoint, Crm2Meeting

# Setup Logger para Debug em Tempo Real
logger = logging.getLogger("copilot")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("copilot_debug.log", encoding="utf-8")
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

# Initialize OpenAI Client
client = None
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define tools (Function Calling schema)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "navigate_to",
            "description": "Comanda o navegador do usuário a navegar para uma URL específica ou página do sistema.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Caminho Exato. Use /projects, /tasks, /kanban, /ia-hub, /meetings, /reports (Relatórios), /crm2/leads (CRM 2)."
                    },
                    "project_search_term": {
                        "type": "string",
                        "description": "Se o usuário pedir para abrir um projeto, coloque aqui o nome dele."
                    },
                    "tab": {
                        "type": "string",
                        "description": "Aba específica dentro do projeto (ex: 'kanban'). Use apenas se o usuário pedir para abrir o kanban/tarefas de um projeto específico."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_meeting",
            "description": "Cria uma nova reunião ('Meeting') no sistema, opcionalmente vinculada a um projeto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date_time": {"type": "string", "description": "Formato YYYY-MM-DD HH:MM:SS"},
                    "project_id": {"type": "integer", "description": "ID do projeto vinculado (se houver)"},
                },
                "required": ["title", "date_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_dashboard",
            "description": "Renderiza gráficos ou componentes visuais dentro do próprio chat para o usuário visualizar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "chart_type": {"type": "string", "enum": ["bar", "pie", "line", "kanban_stats"]},
                    "title": {"type": "string"},
                    "data": {"type": "string", "description": "JSON encodado como string contendo formato apropriado (ex: labels, datasets)"}
                },
                "required": ["chart_type", "title", "data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_project_summary",
            "description": "Busca dados resumidos de um projeto, suas tarefas e status (RAG de projetos).",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {"type": "string", "description": "Nome ou ID do projeto para buscar"}
                },
                "required": ["search_term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_projects",
            "description": "Lista projetos filtrados por nome do projeto, nome do cliente ou status. Use isso para responder perguntas como 'encontre o projeto X' ou 'quais os projetos do cliente Y?'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_search_term": {"type": "string", "description": "Nome ou trecho do nome do projeto para buscar."},
                    "client_search_term": {"type": "string", "description": "Nome do cliente para filtrar os projetos (ex: OAZ, InovaiLab)."},
                    "status_filter": {"type": "string", "description": "Status para filtrar (ex: em_andamento, concluido, pausado)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_lead",
            "description": "Cria um novo Lead no CRM. Use quando o usuário pedir para cadastrar/adicionar um lead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_empresa": {"type": "string"},
                    "nome_contato": {"type": "string"},
                    "email": {"type": "string", "description": "Email do lead (opcional)"},
                    "telefone": {"type": "string", "description": "Telefone do lead (opcional)"},
                    "observacoes": {"type": "string", "description": "Observações ou escopo do lead (opcional)"}
                },
                "required": ["nome_empresa", "nome_contato"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_client",
            "description": "Cria um Cliente Oficial no sistema (CRM 1). Use quando pedirem para criar um cliente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Nome do cliente ou empresa."}
                },
                "required": ["nome"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_project",
            "description": "Cria um novo Projeto associado a um cliente. Diga 'criado' se sucesso.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Título do projeto."},
                    "client_search": {"type": "string", "description": "Nome do cliente para associar (opcional)."}
                },
                "required": ["nome"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Cria uma Tarefa e coloca no Kanban de um projeto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string"},
                    "project_search": {"type": "string", "description": "Nome do projeto onde a tarefa será salva."}
                },
                "required": ["titulo", "project_search"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_subtask",
            "description": "Cria um Item/To-do (Subtarefa) dentro de uma Tarefa existente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "texto": {"type": "string", "description": "O que precisa ser feito."},
                    "task_search": {"type": "string", "description": "Nome da tarefa pai."},
                    "project_search": {"type": "string", "description": "Opcional: Nome do projeto para garantir a tarefa certa caso existam homônimos."},
                    "completed": {"type": "boolean", "description": "Opcional: Definir como 'true' se a subtarefa já nasceu concluída."},
                    "due_date": {"type": "string", "description": "Opcional: Data de vencimento da subtarefa no formato YYYY-MM-DD."}
                },
                "required": ["texto", "task_search"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_pdf_report",
            "description": "Gera um Relatório PDF de um Projeto Específico e manda para download.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_search": {"type": "string", "description": "Qual projeto gerar o PDF?"}
                },
                "required": ["project_search"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_schema",
            "description": "GOD MODE: Retorna o dicionário de todas as Tabelas (Models) do banco de dados e seus campos. Use para mapear as opções antes de editar ou listar algo novo.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_any_entity",
            "description": "Lê registros nativamente de qualquer tabela descoberta via get_system_schema. Retorna os nomes e IDs atuais.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Nome exato do Model. Ex: FinTransaction, Crm2Lead, Task"},
                    "limit": {"type": "integer", "description": "Limite de itens a listar. Máx 30."},
                    "filter_dict": {"type": "object", "description": "Opcional. Dicionário para filtrar resultados exatos. Ex: {'task_id': 55}"}
                },
                "required": ["table_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crud_any_entity",
            "description": "Altera registros no banco. Serve para Update (ex: mudar data, nome), Delete e Move (ex: mudar coluna/status no kanban).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["update", "delete", "move"]},
                    "table_name": {"type": "string", "description": "Nome da tabela. Ex: Task, Client, FinTransaction"},
                    "record_id": {"type": "integer", "description": "O ID do registro a ser alterado."},
                    "payload_json": {"type": "string", "description": "Dicionário JSON de campos a serem alterados. Ex: '{\"status\": \"concluida\"}'. Para delete, mande vazio."}
                },
                "required": ["action", "table_name", "record_id"]
            }
        }
    }
]

def get_system_prompt(user):
    """Gera o prompt do sistema injetando contexto básico do RAG e permissões do usuário."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # RAG Básico: injetando quantos projetos ativos e tarefas ele tem
    # Nota: Em produção, o RAG dinâmico fará consultas granulares. Para o prompt base, limitamos para economizar tokens.
    active_projects = Project.query.filter_by(status='em_andamento').count()
    user_tasks = Task.query.filter_by(assigned_user_id=user.id).count()
    
    prompt = f"""Você é o O ÁS Copilot, o assistente virtual do sistema InovaiLab Gestão.
Você é um desenvolvedor e gerente de projetos hiper-inteligente, integrado nativamente a este ERP/CRM.
Você tem acesso a todas as informações e pode realizar ações executando de forma autônoma (function calling).

[Contexto Atual]
Data e Hora: {current_time}
Usuário Logado: {user.nome} {user.sobrenome} (ID: {user.id})
Nível Admin: {'Sim' if user.is_admin else 'Não'}
Visão Geral: Há {active_projects} projetos em andamento no geral no sistema.
{user.nome} possui {user_tasks} tarefas atribuídas.

[Diretrizes de Onisciência (Você possui controle absoluto)]
1. NAVEGAÇÃO: Se pedirem para "ir para" ou abrir abas, use `navigate_to` de acordo com a URL. SEGREDO DAS URLs ABSOLUTAS: 
Perfil = `/profile` | Dashboard Admin de Usuários = `/admin/users` | Notificações = `/crm2/notifications` | Reuniões = `/meetings`
Kanban Geral = `/kanban` | Kanban no Projeto: `/projects/<id>?tab=kanban` | Relatórios = `/reports` 
Financeiro Dashboard = `/financeiro/dashboard` | Lançamentos = `/financeiro/lancamentos` | Fornecedores = `/financeiro/fornecedores` | Contas = `/financeiro/contas` | Centrais = `/financeiro/centros-custo`.

2. AUTO-DESCOBERTA (GOD MODE): Você se integra a TODO o banco SQL do sistema. Se o usuário perguntar de Lançamentos Financeiros, ou quiser deletar algo "estranho", ou listar Metas, primeiro chame `get_system_schema` para entender o banco de dados.
3. LISTAGENS PODEROSAS: Depois de saber o nome da Tabela, use `list_any_entity` (Ex: table_name="FinTransaction") para listar. Encontre o ID na lista retornada!
4. UPDATE E DELETE NATIVOS: Tendo o ID, se você precisar *mover um cartão no funil*, ou deletar, ou atualizar, use apenas o `crud_any_entity` informando action="update", o ID, e o payload de quais colunas quer sobrescrever. (Use o reflection para ser um deus da programação).
5. CRIAÇÕES OFICIAIS: Continuam valendo suas tools primárias de criação simples (`create_project`, `create_task`, `create_subtask`, `create_lead`, `create_client`).
6. COMPORTAMENTO DE SISTEMA OPERACIONAL: Se afirmarem que você não sabe acessar "notificações", prove o contrário e acesse na hora. Se pedirem pra alterar qualquer vírgula, liste, descubra o ID e DEPOIS faça o UPDATE na lata.
7. Retorne a resposta final sempre em Formatação Markdown amigável e limpa. Não mande JSON pro usuário.
8. PRECISÃO EXTREMA (PROIBIDO CHUTAR NOMES): NUNCA adivinhe ou assuma o nome de um projeto ou tarefa se a intenção do usuário for vaga. Se houver dúvida sobre EM QUAL tarefa/projeto inserir dados, PARE sua execução e pergunte ao usuário para que ele especifique o nome exato do projeto ou tarefa. O erro de inserir dados em tarefas alheias é fatal.
"""
    return prompt

def execute_tool(name, arguments, user):
    """Despacha a execução da tool no backend e retorna a mensagem que deve ser salva ou repassada ao GPT e ao Cliente."""
    try:
        args = json.loads(arguments) if arguments else {}
    except Exception as e:
        args = {}
        print(f"Erro ao fazer parse do Tool Argument JSON: {e}")
    
    if name == "navigate_to":
        url = args.get("url")
        term = args.get("project_search_term")
        tab = args.get("tab")
        
        if url == "/profile":
            return json.dumps({"status": "success", "action": "navigate_to", "url": "/profile", "message": "Acessando Perfil de Usuário."})
        if url == "/admin/users":
            return json.dumps({"status": "success", "action": "navigate_to", "url": "/admin/users", "message": "Abrindo Painel de Controle de Membros."})
        if url == "/crm2/notifications":
            return json.dumps({"status": "success", "action": "navigate_to", "url": "/crm2/notifications", "message": "Acessando notificações."})
            
        if term:
            # Tenta resolver o ID do projeto pelo nome, mas respeitando permissões
            query = Project.query.filter(Project.nome.ilike(f"%{term}%"))
            if not user.is_admin:
                query = query.filter(
                    (Project.responsible_id == user.id) | 
                    (Project.team_members.any(id=user.id))
                )
            
            p = query.first()
            if p:
                url = f"/projects/{p.id}"
                if tab == 'kanban':
                    url += "?tab=kanban"
            else:
                return json.dumps({"status": "error", "message": f"Projeto contendo '{term}' não foi encontrado ou você não tem acesso."})
        elif not url:
            return json.dumps({"status": "error", "message": "Parâmetros 'url' ou 'project_search_term' ausentes."})
            
        # Tratamento de barra inicial caso o robô envie sem 
        if not url.startswith("/"):
            url = "/" + url
            
        # Retorna o payload especial para o frontend interceptar via SSE
        return json.dumps({"status": "success", "action": "navigate_to", "url": url, "message": "Navegando..."})
        
    elif name == "create_meeting":
        # Simula criaçao
        title = args.get("title")
        pid = args.get("project_id")
        return json.dumps({"status": "success", "action": "ui_update", "message": f"Reunião '{title}' criada com sucesso."})
        
    elif name == "generate_dashboard":
        # O chart rendering é handled pelo frontend. Para o backend/GPT, confirmamos que foi enviado.
        return json.dumps({"status": "success", "action": "render_chart", "chart_type": args.get("chart_type"), "data": args.get("data")})
        
    elif name == "get_project_summary":
        term = args.get("search_term")
        pts = Project.query.filter(Project.nome.ilike(f"%{term}%")).limit(5).all()
        res = []
        for p in pts:
            res.append({"id": p.id, "nome": p.nome, "status": p.status, "cliente": p.client.nome if p.client else ""})
        return json.dumps({"status": "success", "results": res})
        
    elif name == "list_projects":
        project_term = args.get("project_search_term")
        client_term = args.get("client_search_term")
        status_filter = args.get("status_filter")
        
        query = Project.query
        if project_term:
            query = query.filter(Project.nome.ilike(f"%{project_term}%"))
        if client_term:
            query = query.join(Client).filter(Client.nome.ilike(f"%{client_term}%"))
        if status_filter:
            query = query.filter(Project.status == status_filter)
            
        pts = query.all()
        if not pts:
            return json.dumps({"status": "success", "message": "Nenhum projeto encontrado com esses filtros.", "action": "chat_reply"})
            
        res_text = f"Encontrei {len(pts)} projetos:\n\n"
        for p in pts:
            client_name = p.client.nome if p.client else "Sem Cliente"
            res_text += f"- **{p.nome}** ({client_name}) - Status: {p.status}\n"
            
        return json.dumps({"status": "success", "action": "chat_reply", "content": res_text})
        
    elif name == "create_lead":
        nome_empresa = args.get("nome_empresa")
        nome_contato = args.get("nome_contato")
        email = args.get("email")
        telefone = args.get("telefone")
        obs = args.get("observacoes")
        
        if not nome_empresa or not nome_contato:
            return json.dumps({"status": "error", "message": "Faltam dados obrigatórios (nome_empresa, nome_contato)."})
            
        new_lead = Crm2Lead(
            nome_empresa=nome_empresa,
            nome_contato=nome_contato,
            email=email,
            telefone=telefone,
            observacoes=obs,
            estagio='Lead'
        )
        db.session.add(new_lead)
        db.session.commit()
        
        return json.dumps({
            "status": "success", 
            "action": "chat_reply", 
            "content": f"Lead '{nome_empresa}' (Contato: {nome_contato}) criado com sucesso no CRM!"
        })

    elif name == "create_client":
        nome = args.get("nome")
        c = Client(nome=nome, creator_id=user.id)
        db.session.add(c)
        db.session.commit()
        return json.dumps({"status": "success", "action": "ui_update", "message": f"Cliente oficial '{nome}' criado no sistema."})

    elif name == "create_project":
        nome = args.get("nome")
        client_search = args.get("client_search")
        
        client_id = None
        if client_search:
            c = Client.query.filter(Client.nome.ilike(f"%{client_search}%")).first()
            if c: client_id = c.id
            
        if not client_id:
            c = Client.query.first() # fallback caso não passe e não ache (devido à obrigatoriedade da foreign key em models antigos)
            client_id = c.id if c else 1

        p = Project(nome=nome, client_id=client_id, responsible_id=user.id)
        db.session.add(p)
        db.session.commit()
        # Adiciona criador à equipe
        p.team_members.append(user)
        db.session.commit()
        return json.dumps({"status": "success", "action": "ui_update", "message": f"Projeto '{nome}' criado com sucesso e adicionado aos seus projetos."})

    elif name == "create_task":
        titulo = args.get("titulo")
        project_search = args.get("project_search")
        
        p = Project.query.filter(Project.nome.ilike(f"%{project_search}%")).first()
        if not p:
            return json.dumps({"status": "error", "message": f"Não encontrei um projeto com o nome '{project_search}'."})
            
        t = Task(titulo=titulo, project_id=p.id, assigned_user_id=user.id)
        db.session.add(t)
        db.session.commit()
        return json.dumps({"status": "success", "action": "ui_update", "message": f"Tarefa '{titulo}' salva no projeto {p.nome}."})

    elif name == "create_subtask":
        texto = args.get("texto")
        task_search = args.get("task_search")
        project_search = args.get("project_search")
        completed = args.get("completed", False)
        due_date_str = args.get("due_date", None)
        
        query = Task.query.filter(Task.titulo.ilike(f"%{task_search}%"))
        
        if project_search:
            p = Project.query.filter(Project.nome.ilike(f"%{project_search}%")).first()
            if p:
                query = query.filter(Task.project_id == p.id)
            else:
                return json.dumps({"status": "error", "message": f"Projeto '{project_search}' não encontrado para filtrar a tarefa."})
                
        t = query.first()
        
        if not t:
            return json.dumps({"status": "error", "message": f"Não encontrei a tarefa '{task_search}'. Peça mais detalhes ao usuário."})
            
        due_date_obj = None
        if due_date_str:
            try:
                due_date_obj = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except Exception:
                pass
                
        si = TodoItem(
            texto=texto, 
            task_id=t.id, 
            completed=completed,
            due_date=due_date_obj
        )
        if completed:
            si.completed_at = datetime.utcnow()
            
        db.session.add(si)
        db.session.commit()
        return json.dumps({"status": "success", "action": "ui_update", "message": f"To-do '{texto}' inserido na tarefa {t.titulo} (Concluído: {completed})."})

    elif name == "generate_pdf_report":
        term = args.get("project_search")
        p = Project.query.filter(Project.nome.ilike(f"%{term}%")).first()
        if not p: return json.dumps({"status": "error", "message": "Projeto não encontrado."})
        
        # Como o download em si precisa vir do navegador via form POST (devido ao header content-disposition de binário do PDF), 
        # Nós usamos Action JSON pro widget disparar o fetch ou form nativo!
        return json.dumps({"status": "success", "action": "download_pdf", "project_id": p.id, "message": f"Relatório do projeto '{p.nome}' gerado! O download vai começar em instantes."})

    elif name == "get_system_schema":
        SCHEMA_MAP = {
            "User": "id, nome, sobrenome, email, is_admin, ativo",
            "Client": "id, nome, email, telefone, empresa, endereco",
            "Project": "id, nome, status, progress_percent, client_id",
            "Task": "id, titulo, descricao, status (pendente, em_andamento, concluida), project_id, ordem",
            "TodoItem": "id, texto, completed (bool), task_id, due_date",
            "Crm2Lead": "id, nome_empresa, nome_contato, estagio (ex: Lead, Qualificação, Fechado)",
            "FinCostCenter": "id, nome",
            "FinAccount": "id, nome, tipo (wallet/credit_card)",
            "FinTransaction": "id, tipo (income/expense), valor, data, descricao, account_id",
            "FinSupplier": "id, nome"
        }
        return json.dumps({"status": "success", "schema": SCHEMA_MAP})

    elif name == "list_any_entity":
        table_name = args.get("table_name")
        limit = args.get("limit", 15)
        filter_dict = args.get("filter_dict", {})
        
        # Mapa dinamico de classes
        models_dict = {
            "User": User, "Client": Client, "Project": Project,
            "Task": Task, "TodoItem": TodoItem, "Crm2Lead": Crm2Lead,
            "FinCostCenter": FinCostCenter, "FinAccount": FinAccount,
            "FinTransaction": FinTransaction, "FinSupplier": FinSupplier
        }
        
        ModelClass = models_dict.get(table_name)
        if not ModelClass:
            return json.dumps({"status": "error", "message": f"Tabela '{table_name}' desconhecida ou não mapeada no God Mode."})
            
        try:
            query = ModelClass.query
            if isinstance(filter_dict, dict):
                for k, v in filter_dict.items():
                    if hasattr(ModelClass, k):
                        query = query.filter(getattr(ModelClass, k) == v)
                        
            records = query.limit(limit).all()
            results = []
            for r in records:
                # Usa dict comprehension pra tentar pegar propriedades basicas sem explodir
                res_dict = {"id": getattr(r, "id", None)}
                if hasattr(r, "nome"): res_dict["nome"] = r.nome
                if hasattr(r, "titulo"): res_dict["titulo"] = r.titulo
                if hasattr(r, "nome_empresa"): res_dict["nome_empresa"] = r.nome_empresa
                if hasattr(r, "descricao"): res_dict["descricao"] = r.descricao
                if hasattr(r, "status"): res_dict["status"] = r.status
                if hasattr(r, "estagio"): res_dict["estagio"] = getattr(r, "estagio")
                if hasattr(r, "valor"): res_dict["valor"] = getattr(r, "valor")
                if hasattr(r, "texto"): res_dict["texto"] = getattr(r, "texto")
                if hasattr(r, "task_id"): res_dict["task_id"] = getattr(r, "task_id")
                results.append(res_dict)
                
            return json.dumps({"status": "success", "table": table_name, "count": len(results), "data": results})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    elif name == "crud_any_entity":
        action = args.get("action")
        table_name = args.get("table_name")
        record_id = args.get("record_id")
        payload = args.get("payload_json", "{}")
        
        models_dict = {
            "User": User, "Client": Client, "Project": Project,
            "Task": Task, "TodoItem": TodoItem, "Crm2Lead": Crm2Lead,
            "FinCostCenter": FinCostCenter, "FinAccount": FinAccount,
            "FinTransaction": FinTransaction, "FinSupplier": FinSupplier
        }
        
        ModelClass = models_dict.get(table_name)
        if not ModelClass:
            return json.dumps({"status": "error", "message": "Model desconhecido."})
            
        record = ModelClass.query.get(record_id)
        if not record:
            return json.dumps({"status": "error", "message": f"Registro {record_id} na tabela {table_name} não encontrado."})
            
        if action == "delete":
            db.session.delete(record)
            db.session.commit()
            return json.dumps({"status": "success", "action": "ui_update", "message": f"Registro {table_name} (id {record_id}) deletado à força."})
            
        elif action in ["update", "move"]:
            try:
                if isinstance(payload, dict):
                    updates = payload
                else:
                    updates = json.loads(payload)
                    
                for key, val in updates.items():
                    if hasattr(record, key):
                        setattr(record, key, val)
                db.session.commit()
                return json.dumps({"status": "success", "action": "ui_update", "message": f"Registro {table_name} (id {record_id}) modificado com: {payload}"})
            except Exception as e:
                db.session.rollback()
                return json.dumps({"status": "error", "message": f"Erro no JSON Payload de update: {str(e)}"})

    return json.dumps({"status": "error", "message": "Unknown tool"})

def chat_stream(user_id, user_message):
    """
    Motor do Copilot:
    1. Grava msg do user
    2. Lê histórico (ultimas 10)
    3. Chama OpenAI
    4. Avalia Tool Calling
    5. Retorna o texto + eventos pro client
    """
    user = db.session.get(User, user_id)
    if not user:
        yield "data: " + json.dumps({"error": "User not found"}) + "\n\n"
        return
        
    if not client:
        yield "data: " + json.dumps({"error": "OPENAI_API_KEY não configurada no .env"}) + "\n\n"
        return

    # Salva no banco
    msg = AiChatHistory(user_id=user.id, role='user', content=user_message)
    db.session.add(msg)
    db.session.commit()
    
    # Montar histórico pro GPT
    history = AiChatHistory.query.filter_by(user_id=user.id).order_by(AiChatHistory.created_at.desc()).limit(15).all()
    history.reverse() # Cronológico
    
    messages = [{"role": "system", "content": get_system_prompt(user)}]
    for h in history:
        # Tratamento basico p/ roles validos
        if h.role in ['user', 'assistant']:
            messages.append({"role": h.role, "content": h.content or ""})
            
    try:
        iteration = 0
        max_iterations = 15 # Aumentado para 15 (Seguro para multi-ações complexas)
        
        while iteration < max_iterations:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                stream=False
            )
            
            response_message = completion.choices[0].message
            tool_calls = response_message.tool_calls
            
            if tool_calls:
                logger.info(f"GPT solicitou {len(tool_calls)} tool calls na iteração {iteration+1}.")
                
                # Adiciona a listagem de ferramentas invocadas ao histórico
                messages.append(response_message)
                
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments
                    
                    logger.info(f"Executando {function_name} args: {function_args}")
                    try:
                        tool_result = execute_tool(function_name, function_args, user)
                        logger.debug(f"{function_name} Result: {str(tool_result)[:100]}")
                    except Exception as e:
                        logger.error(f"Erro em {function_name}: {str(e)}", exc_info=True)
                        tool_result = json.dumps({"status": "error", "message": f"Erro interno: {str(e)}"})
                    
                    # Avisa a UI sobre o status em andamento
                    action_text = "Processando banco de dados..."
                    try:
                        res_json = json.loads(tool_result)
                        action_text = res_json.get("action", res_json.get("message", function_name))
                    except: pass
                    
                    yield f"data: {json.dumps({'status': 'success', 'action': action_text})}\n\n"
                    
                    # Anexa o resultado da tool ao script system prompt pra OpenAI prosseguir
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result
                    })
                    
                    # Salva no banco de intents
                    sys_msg = AiChatHistory(user_id=user.id, role='assistant', tool_calls=function_args, tool_call_id=function_name)
                    db.session.add(sys_msg)
                    tool_msg = AiChatHistory(user_id=user.id, role='tool', content=tool_result)
                    db.session.add(tool_msg)
                    
                db.session.commit()
                iteration += 1
                
                # E o looping roda novamente mandando o resultado pro GPT entender!
                logger.info(f"Progredindo para Fase {iteration+1} do motor reflexivo...")
                
            else:
                # O GPT devolveu texto limpo. Fim do Multi-turn.
                content = response_message.content
                logger.info(f"Resposta Final do GPT finalizada: {str(content)[:100]}...")
                
                ai_msg = AiChatHistory(user_id=user.id, role='assistant', content=content)
                db.session.add(ai_msg)
                db.session.commit()
                
                yield f"data: {json.dumps({'content': content})}\n\n"
                yield "data: [DONE]\n\n"
                break
                
        if iteration >= max_iterations:
            final_msg = "Atingi meu limite de processamento (15 etapas contínuas) para proteger a integridade do sistema. Se eu não terminei sua solicitação, por favor, peça para eu continuar de onde parei!"
            ai_msg = AiChatHistory(user_id=user.id, role='assistant', content=final_msg)
            db.session.add(ai_msg)
            db.session.commit()
            yield f"data: {json.dumps({'content': final_msg})}\n\n"
            yield "data: [DONE]\n\n"
            
    except Exception as e:
        logger.error(f"Fatal copilot error: {e}", exc_info=True)
        yield f"data: {json.dumps({'error': str(e), 'message': f'Houve uma falha fatal no motor: {str(e)}'})}\n\n"
        yield "data: [DONE]\n\n"
