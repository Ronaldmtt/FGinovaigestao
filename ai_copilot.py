import os
import json
import logging
from datetime import datetime
from openai import OpenAI
from extensions import db
from models import AiChatHistory, User, Project, Task, Meeting, Client, Crm2Lead

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
                        "description": "Caminho (ex: /projects, /kanban). Use isso SOMENTE se não for um projeto específico."
                    },
                    "project_search_term": {
                        "type": "string",
                        "description": "Se o usuário pedir para abrir um projeto, coloque aqui o nome do projeto (ex: Inadimplência, FinOps). O sistema resolverá o ID correto."
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
            "description": "Lista projetos filtrados por nome do cliente ou status. Use isso para responder perguntas como 'quais os projetos do cliente X?' ou 'quais projetos estão abertos?'.",
            "parameters": {
                "type": "object",
                "properties": {
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

[Diretrizes]
1. Se o usuário pedir para navegar ou abrir "a tela X", use a função `navigate_to`. As telas base são /projects, /tasks, /kanban, /ia-hub, /meetings.
2. Se o usuário pedir para abrir um projeto Específico, mande o parâmetro `project_search_term` na tool `navigate_to`. O sistema cuidará de encontrar e abrir a URL certa. Nunca adivinhe ou crie a URL do projeto sozinho.
3. Se o usuário pedir para listar projetos (de um cliente específico, ou em andamento), mande o parâmetro `client_search_term` na tool `list_projects`. O sistema irá buscar no banco de dados e devolver a lista para você mostrar ao usuário.
4. Se o usuário pedir para criar um LEAD, chame imediatamente a ferramenta `create_lead`. Caso não tenha o NOME DA EMPRESA e NOME DO CONTATO, pergunte a ele antes de chamar a tool.
5. Fale com naturalidade, seja objetivo. Se for criar algo, verifique explicitamente se possui as variáveis ou peça ao usuário o que falta.
6. Analise pedidos gráficos e use `generate_dashboard` com dados falsos úteis/exemplos ou dados reais quando extraídos de `get_project_summary`.
7. Suas respostas de chat devem usar Markdown com clareza.
"""
    return prompt

def execute_tool(name, arguments, user):
    """Despacha a execução da tool no backend e retorna a mensagem que deve ser salva ou repassada ao GPT e ao Cliente."""
    args = json.loads(arguments)
    
    if name == "navigate_to":
        url = args.get("url")
        term = args.get("project_search_term")
        
        if term:
            # Tenta resolver o ID do projeto pelo nome
            p = Project.query.filter(Project.nome.ilike(f"%{term}%")).first()
            if p:
                url = f"/projects/{p.id}"
            else:
                return json.dumps({"status": "error", "message": f"Projeto contendo '{term}' não foi encontrado."})
        elif not url:
            return json.dumps({"status": "error", "message": "Parâmetros 'url' ou 'project_search_term' ausentes."})
            
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
        client_term = args.get("client_search_term")
        status_filter = args.get("status_filter")
        
        query = Project.query
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
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            stream=False # Para simplicidade na primeira iteração do copilot
        )
        
        response_message = completion.choices[0].message
        tool_calls = response_message.tool_calls
        
        # O GPT decidiu usar uma tool
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments
                
                # Executa
                tool_result = execute_tool(function_name, function_args, user)
                
                # Avisa a UI que uma tool foi disparada (front vai escutar esse JSON)
                yield f"data: {tool_result}\n\n"
                
                # Salva a intent no banco 
                sys_msg = AiChatHistory(user_id=user.id, role='assistant', tool_calls=function_args, tool_call_id=function_name)
                db.session.add(sys_msg)
                
                tool_msg = AiChatHistory(user_id=user.id, role='tool', content=tool_result)
                db.session.add(tool_msg)
                
            db.session.commit()
            
            # Aqui poderíamos fazer uma 2a chamada à OpenAI para relatar o sucesso do tool calling pro usuario,
            # Mas vamos encerrar emitindo DONE.
            yield "data: [DONE]\n\n"
            
        else:
            # Resposta pular normal (Texto)
            content = response_message.content
            ai_msg = AiChatHistory(user_id=user.id, role='assistant', content=content)
            db.session.add(ai_msg)
            db.session.commit()
            
            # Manda em chunk unico (ou poderiamos streamar)
            yield f"data: {json.dumps({'content': content})}\n\n"
            yield "data: [DONE]\n\n"
            
    except Exception as e:
        logging.error(f"OpenAI Error: {str(e)}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
