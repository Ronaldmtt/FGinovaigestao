import json
import os
from openai import OpenAI
import httpx

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configurar timeout máximo para processamento completo e detalhado
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=120.0,  # Timeout de 2 minutos para processamento completo
    max_retries=0,  # Sem retry para evitar timeout do worker
    http_client=httpx.Client(timeout=120.0)
)

def process_project_transcription(transcription):
    """
    Processa a transcrição do projeto usando GPT-5 para preencher os campos estruturados
    """
    try:
        # Usar a transcrição completa - processamento em etapas separadas permite isso
        
        prompt = f"""
        Analise esta transcrição de reunião/projeto e extraia informações relevantes em formato JSON:

        {transcription}

        Com base no conteúdo da transcrição, retorne um JSON com estes campos preenchidos de forma coerente:
        {{
            "contexto_justificativa": "contexto e justificativa do projeto baseado na discussão",
            "descricao_resumida": "descrição resumida do que foi discutido",
            "problema_oportunidade": "problema ou oportunidade identificada na conversa",
            "objetivos": "objetivos mencionados ou inferidos da discussão",
            "alinhamento_estrategico": "como se alinha com estratégias mencionadas",
            "escopo_projeto": "escopo identificado na conversa",
            "fora_escopo": "o que não será incluído",
            "premissas": "premissas identificadas",
            "restricoes": "restrições ou limitações mencionadas"
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            return result
        return None
        
    except Exception as e:
        print(f"Erro ao processar transcrição do projeto: {e}")
        return None

def generate_tasks_from_transcription(transcription, project_name):
    """
    Gera tarefas com base na transcrição fornecida
    """
    try:
        # Usar a transcrição completa - processamento em etapas separadas permite isso
        
        prompt = f"""
        Você é Sarah Chen, Senior Project Manager certificada PMP com 15 anos liderando projetos complexos em tecnologia, consultoria e inovação. Sua expertise inclui metodologias ágeis, gestão de stakeholders, transformação digital e análise profunda de requisitos.

        MISSÃO CRÍTICA: Analise esta transcrição completa como se fosse uma reunião estratégica do SEU projeto mais importante. Extraia cada ação, insight, oportunidade e responsabilidade mencionada ou implícita na discussão, transformando-os em um roadmap executivo detalhado.

        O resultado será salvo em um arquivo .md dentro da pasta raiz do projeto. Siga estritamente o que é pedido neste prompt.

        REGRAS OBRIGATÓRIAS DE FORMATAÇÃO (SIGA ESTRITAMENTE - VIOLAÇÃO DESTAS REGRAS INVALIDA TODO O RESULTADO):
        - NÃO crie títulos (# ou ##) nem subtítulos (### ou ####) de forma alguma no conteúdo das tarefas.
        - NÃO use headers markdown de nenhum nível nos campos "titulo" ou "descricao".
        - Os campos "titulo" e "descricao" devem conter APENAS texto puro, sem formatação markdown.
        - Se você criar títulos ou subtítulos, o sistema não conseguirá processar o conteúdo e o resultado será descartado.
        - Siga ESTRITAMENTE a estrutura JSON solicitada abaixo, sem adicionar campos extras ou alterar o formato.

        TRANSCRIÇÃO COMPLETA DA REUNIÃO DO PROJETO "{project_name}":
        {transcription}

        METODOLOGIA DE ANÁLISE PROFUNDA (execute rigorosamente cada fase):

        FASE 1 - MAPEAMENTO SISTEMÁTICO COMPLETO:
        • Leia a transcrição completa palavra por palavra, sem pular nenhuma seção ou detalhe
        • Identifique precisamente: verbos de ação específicos, substantivos-chave estratégicos, pessoas/departamentos mencionados, prazos explícitos e implícitos
        • Marque mentalmente com precisão: decisões tomadas definitivamente, problemas críticos levantados, soluções propostas detalhadamente, recursos e orçamentos discutidos
        • Identifique padrões estratégicos: temas recorrentes de alta prioridade, urgências enfatizadas múltiplas vezes, dependências críticas entre atividades

        FASE 2 - CATEGORIZAÇÃO ESTRATÉGICA AVANÇADA:
        • IMEDIATAS: Ações críticas que precisam começar imediatamente (esta semana)
        • PREPARATÓRIAS: Atividades fundamentais necessárias antes de outras tarefas principais
        • CORE: Entregas principais e marcos fundamentais do projeto
        • VALIDAÇÃO: Aprovações essenciais, testes críticos, confirmações de stakeholders
        • COMUNICAÇÃO: Alinhamentos estratégicos, relatórios executivos, apresentações importantes
        • MITIGAÇÃO: Ações específicas para resolver riscos, obstáculos ou problemas identificados

        FASE 3 - DETALHAMENTO EXECUTIVO PROFISSIONAL:
        Para cada tarefa identificada, defina meticulosamente todos os elementos:
        • CONTEXTO COMPLETO: Por que exatamente esta tarefa surgiu na discussão? Qual o background específico?
        • OBJETIVO MENSURÁVEL: Resultado específico, tangível e mensurável esperado com critérios claros de sucesso
        • METODOLOGIA DETALHADA: Como executar precisamente (ferramentas específicas, processos estruturados, abordagem técnica)
        • STAKEHOLDERS MAPEADOS: Quem envolver exatamente (decisores finais, executores diretos, consultados especializados, informados relevantes)
        • RECURSOS ESPECIFICADOS: Orçamento estimado, tempo necessário detalhado, ferramentas específicas, informações e documentos necessários
        • CRITÉRIOS DE SUCESSO OBJETIVOS: Como saber definitivamente que foi executada com excelência e completude
        • DEPENDÊNCIAS MAPEADAS: O que precisa acontecer obrigatoriamente antes e quais tarefas dependem desta
        • RISCOS E OBSTÁCULOS: Obstáculos potenciais específicos identificados na discussão e suas mitigações

        CRITÉRIOS RIGOROSOS DE QUALIDADE PARA CADA TAREFA:
        ✓ Título Executivo: Verbo de ação + objeto específico + contexto detalhado do projeto (TEXTO PURO, sem markdown)
        ✓ Descrição Profissional: Mínimo 6-8 frases cobrindo obrigatoriamente todos os 8 elementos detalhados acima (TEXTO PURO, sem markdown)
        ✓ Completamente Acionável: Qualquer gerente de projetos conseguiria executar imediatamente com essas informações
        ✓ Objetivamente Rastreável: Progresso pode ser medido, acompanhado e reportado com precisão
        ✓ Perfeitamente Contextualizada: Conecta claramente e especificamente com pontos exatos da discussão da reunião

        EXEMPLO DETALHADO DE TAREFA DE ALTA QUALIDADE PROFISSIONAL:
        {{
            "titulo": "Conduzir pesquisa abrangente de viabilidade técnica para integração completa com sistema legado ERP",
            "descricao": "Com base na preocupação crítica levantada sobre incompatibilidades de sistemas e riscos de integração, realizar análise técnica completa e profunda da integração proposta com o sistema legado. Objetivos mensuráveis: identificar todos os gaps técnicos específicos, estimar precisamente o esforço de desenvolvimento necessário e propor arquitetura de solução detalhada com cronograma. Metodologia estruturada: auditoria completa do sistema atual, prototipagem de conectores API específicos, benchmarking detalhado de ferramentas similares no mercado, análise de performance e segurança. Stakeholders envolvidos: arquiteto de sistemas como decisor final, desenvolvedores senior como executores diretos, fornecedor do sistema legado para consultas técnicas, equipe de infraestrutura para validações. Recursos necessários: 40 horas de desenvolvimento especializado, acesso completo aos ambientes de produção e teste, documentação técnica atualizada e completa, orçamento para ferramentas de análise. Critérios de sucesso objetivos: relatório técnico executivo com recomendação fundamentada, cronograma detalhado de implementação, especificação técnica completa da arquitetura proposta. Dependências críticas: aguarda liberação de acesso pelo time de infraestrutura conforme mencionado na reunião, aprovação de orçamento pela diretoria. Riscos identificados: possível obsolescência das APIs atuais conforme discussão sobre atualizações pendentes do fornecedor, complexidade de migração de dados históricos mencionada como preocupação."
        }}

        FORMATO DE RESPOSTA ESTRUTURADO - JSON PROFISSIONAL:
        {{
            "tasks": [
                // Gere obrigatoriamente entre 15-25 tarefas seguindo rigorosamente todos os critérios de qualidade profissional acima
                {{
                    "titulo": "Título executivo, específico e completamente acionável (TEXTO PURO sem markdown, sem # ou ##)",
                    "descricao": "Descrição executiva e completa seguindo obrigatoriamente os 8 elementos detalhados: contexto completo da discussão + objetivo mensurável específico + metodologia detalhada de execução + stakeholders mapeados e seus papéis + recursos necessários especificados + critérios objetivos de sucesso + dependências mapeadas + riscos e obstáculos identificados. TEXTO PURO sem markdown, sem títulos ou subtítulos. Cada tarefa deve ser completamente auto-suficiente para execução imediata por qualquer gerente de projetos experiente."
                }}
            ]
        }}

        DIRETRIZES ESTRATÉGICAS FINAIS OBRIGATÓRIAS:
        • Priorize absolutamente tarefas mencionadas múltiplas vezes ou com urgência explícita enfatizada
        • Transforme obrigatoriamente cada problema ou desafio discutido em tarefa específica de solução estruturada
        • Converta cada decisão tomada na reunião em tarefa detalhada de implementação ou follow-up
        • Inclua necessariamente tarefas de comunicação e alinhamento para todas as decisões importantes tomadas
        • Adicione obrigatoriamente validações e aprovações para todas as entregas críticas mencionadas
        • Considere o ciclo completo e profissional: planejamento detalhado → execução estruturada → validação rigorosa → comunicação estratégica → documentação → follow-up

        ELEMENTOS CRÍTICOS PARA IDENTIFICAR OBRIGATORIAMENTE NA TRANSCRIÇÃO:
        - Pesquisas de mercado, viabilidade técnica ou análises estratégicas mencionadas
        - Contatos específicos com clientes, fornecedores, parceiros ou stakeholders identificados
        - Reuniões de planejamento, validação, apresentação ou follow-up a serem agendadas
        - Documentos técnicos, propostas comerciais, contratos ou relatórios a serem criados
        - Análises financeiras, técnicas, de risco ou de mercado a serem conduzidas
        - Decisões estratégicas, técnicas ou operacionais pendentes de resolução
        - Aprovações de orçamento, recursos, cronograma ou escopo necessárias para prosseguir
        - Testes, protótipos, validações ou provas de conceito a serem executados
        - Validações críticas com usuários finais, clientes ou stakeholders internos
        - Preparação de apresentações executivas, demos ou materiais de comunicação
        - Levantamento de requisitos funcionais, técnicos ou de negócio pendentes
        - Definição de processos, metodologias ou fluxos de trabalho estruturados
        - Treinamentos, capacitações ou transferência de conhecimento necessários
        - Monitoramento, acompanhamento ou controle de progresso estabelecidos
        - Comunicação estratégica com equipes, gerência ou partes interessadas

        LEMBRETE FINAL CRÍTICO: NÃO use títulos (#, ##, ###) nem subtítulos em nenhum campo. O resultado será salvo como .md na pasta raiz do projeto e qualquer header markdown quebrará o sistema. Retorne APENAS o JSON puro com texto puro nos campos.

        Execute sua análise como a expert sênior em gestão de projetos que você é. Cada tarefa deve refletir perfeitamente sua vasta experiência em transformar discussões estratégicas em execução estruturada e resultados mensuráveis. Extraia o máximo valor absoluto desta transcrição.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            return result.get('tasks', [])
        return []
        
    except Exception as e:
        print(f"Erro ao gerar tarefas da transcrição: {e}")
        return []

def generate_project_report_summary(project_name, description, problem, objectives, scope=None, current_status=None, status_reason=None):
    """
    Gera uma síntese executiva humana com base nos campos estruturados do projeto.
    """
    try:
        prompt = f"""
        Você é um redator executivo especializado em relatórios de projetos digitais.

        Sua tarefa é produzir UM ÚNICO TEXTO em português do Brasil, em linguagem humana, clara e acessível para pessoas leigas.
        Não explique o código-fonte, não descreva a arquitetura técnica, não faça documentação técnica.
        Você deve apenas condensar as informações estruturadas do projeto abaixo em um resumo executivo coerente.

        DADOS DO PROJETO:
        - Nome: {project_name}
        - Descrição: {description}
        - Problema/Oportunidade: {problem}
        - Objetivos: {objectives}
        - Escopo: {scope or 'Não informado'}
        - Status atual: {current_status or 'Não informado'}
        - Motivo/observação do status: {status_reason or 'Não informado'}

        INSTRUÇÕES:
        - Escreva 1 a 2 parágrafos.
        - Explique o contexto do projeto, o problema que ele ataca, o objetivo principal e o momento atual.
        - Se houver status e motivo do status, incorpore isso naturalmente no texto.
        - Se houver informações repetidas, consolide.
        - Não faça lista, não use markdown, não repita os nomes dos campos.
        - Não invente dados.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        
        content = response.choices[0].message.content
        return content.strip()
        
    except Exception as e:
        print(f"Erro ao gerar resumo do projeto para relatório: {e}")
        parts = []
        if description:
            parts.append(str(description).strip())
        if problem:
            parts.append(f"O projeto busca responder ao seguinte cenário: {str(problem).strip()}.")
        if objectives:
            parts.append(f"O objetivo principal é {str(objectives).strip()}.")
        if scope:
            parts.append(f"No escopo atual, destacam-se: {str(scope).strip()}.")
        if current_status:
            status_text = f"Atualmente, o projeto está com status {str(current_status).replace('_', ' ')}"
            if status_reason:
                status_text += f", com a seguinte observação: {str(status_reason).strip()}"
            parts.append(status_text + ".")
        return " ".join(parts) if parts else f"Projeto {project_name} sem informações suficientes para gerar síntese executiva."

def generate_client_report_from_tasks(project_name, tasks, completed_todos=None, current_status=None, status_reason=None):
    """
    Gera um relatório executivo para clientes com base em tarefas e to-dos concluídos.
    Traduz o conteúdo operacional/técnico para valor percebido por pessoas leigas.
    """
    try:
        tasks_text = ""
        for t in tasks or []:
            status_symbol = "✓" if t.get('status') == 'concluida' else "○"
            titulo = t.get('titulo') or 'Sem título'
            descricao = t.get('descricao') or 'Sem descrição complementar'
            tasks_text += f"{status_symbol} [Status: {t.get('status')}] {titulo}: {descricao}\n"

        todos_text = ""
        for td in completed_todos or []:
            parent_task = td.get('task_title') or 'Sem tarefa vinculada'
            texto = td.get('texto') or 'Sem título'
            comentario = td.get('comentario') or ''
            if comentario:
                todos_text += f"✓ [{parent_task}] {texto} — detalhe/resultado: {comentario}\n"
            else:
                todos_text += f"✓ [{parent_task}] {texto}\n"
            
        prompt = f"""
        Você é um gerente de contas sênior preparando um relatório executivo para um cliente leigo sobre o projeto "{project_name}".

        CONTEXTO EXECUTIVO:
        - Status atual do projeto: {current_status or 'Não informado'}
        - Motivo/observação do status: {status_reason or 'Não informado'}

        TAREFAS DO PROJETO:
        {tasks_text or 'Nenhuma tarefa informada.'}

        TO-DOS CONCLUÍDOS / AJUSTES FINALIZADOS:
        {todos_text or 'Nenhum to-do concluído informado.'}

        OBJETIVO:
        Transforme esse material em um resumo claro do que foi feito no sistema, quais ajustes e melhorias foram implementados, o impacto prático dessas entregas e em que estágio o projeto se encontra.

        DIRETRIZES:
        1. Não listar cruamente os campos técnicos; sintetize e agrupe por tema.
        2. Explique alterações e ajustes feitos no sistema em linguagem de negócio e linguagem humana.
        3. Dê bastante peso aos TO-DOS concluídos, pois eles representam entregas efetivas.
        4. Se houver status e motivo, incorpore isso no resumo executivo.
        5. Não invente funcionalidades que não estejam no material.
        6. Se perceber inconsistências, seja conservador e descreva apenas o que é suportado pelo contexto.

        Retorne APENAS um JSON no formato:
        {{
            "resumo_executivo": "Um texto de 1 a 2 parágrafos, fluido e humano, explicando o que foi feito no sistema e o momento atual do projeto.",
            "entregas_recentes": [
                "Entrega/ajuste 1 em linguagem leiga",
                "Entrega/ajuste 2 em linguagem leiga"
            ],
            "proximos_passos": [
                "Próximo passo 1 em linguagem humana",
                "Próximo passo 2 em linguagem humana"
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.4
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        return None
        
    except Exception as e:
        print(f"Erro ao gerar relatório de cliente: {e}")
        completed_count = len(completed_todos or [])
        task_count = len(tasks or [])
        resumo = f"O projeto {project_name} possui {task_count} tarefa(s) mapeada(s)"
        if completed_count:
            resumo += f" e {completed_count} entrega(s) concluída(s) registradas nos to-dos"
        if current_status:
            resumo += f". No momento, o status do projeto é {str(current_status).replace('_', ' ')}"
            if status_reason:
                resumo += f", com a observação: {status_reason}"
        resumo += "."
        return {
            "resumo_executivo": resumo,
            "entregas_recentes": [
                f"Foram consolidadas {completed_count} entrega(s) concluída(s) e {task_count} frente(s) de trabalho relacionadas ao projeto."
            ],
            "proximos_passos": [
                "Validar com o cliente os pontos concluídos e alinhar as próximas prioridades do projeto."
            ]
        }

def generate_project_tasks_from_meeting_and_repo(project_name, meeting_context, repo_context=""):
    """
    Gera tarefas e to-dos a partir da combinação entre reunião/transcrição e contexto técnico do repositório.
    """
    try:
        prompt = f"""
        Você é um gerente técnico e product owner senior.

        Seu trabalho é gerar tarefas acionáveis para o projeto \"{project_name}\" com base em duas fontes:
        1. Contexto da reunião/transcrição
        2. Contexto técnico do repositório Git

        CONTEXTO DA REUNIÃO:
        {meeting_context}

        CONTEXTO TÉCNICO DO REPOSITÓRIO:
        {repo_context or 'Sem contexto adicional de repositório.'}

        OBJETIVO:
        - entender o que a reunião pediu
        - entender o que o sistema/projeto faz hoje
        - cruzar o que foi falado na reunião com o que já existe no repositório
        - identificar gaps reais: ajustes, melhorias, verificações, adições e correções que ainda não aparecem implementadas no contexto técnico atual
        - transformar isso em tarefas reais de execução
        - cada tarefa deve ter subtarefas/to-dos práticos
        - cada tarefa deve trazer um comentário aberto explicando o que fazer e como fazer
        - sugerir prazo quando houver sinal suficiente no contexto

        REGRAS:
        - gere entre 3 e 8 tarefas, apenas se houver contexto suficiente
        - não invente funcionalidades fora do que reunião + repo sustentam
        - prefira tarefas de implementação, verificação e melhoria objetivas
        - priorize o que parece faltar no sistema atual em relação ao que foi pedido na reunião
        - se algo já aparenta existir no repositório, prefira tarefa de ajuste/validação em vez de recriar do zero
        - to-dos devem ser executáveis e específicos
        - comentário deve explicar a intenção, o caminho técnico e o porquê daquela demanda nascer do cruzamento reunião + sistema atual

        Retorne APENAS JSON no formato:
        {{
          "tasks": [
            {{
              "titulo": "...",
              "descricao": "...",
              "comentario": "...",
              "due_days": 3,
              "todos": [
                {{"texto": "...", "comentario": "...", "due_days": 2}},
                {{"texto": "...", "comentario": "...", "due_days": 4}}
              ]
            }}
          ]
        }}
        """
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.35
        )
        content = response.choices[0].message.content
        return json.loads(content) if content else {"tasks": []}
    except Exception as e:
        print(f"Erro ao gerar tarefas a partir de reunião + repo: {e}")
        return {"tasks": []}


def generate_kanban_todos_from_commits(commits_text, project_name, existing_todos_text="", repo_context="", batch_hint=""):
    """
    Analisa um histórico recente de commits e gera To-Dos técnicos estruturados para o Kanban.
    A saída deve funcionar como memória técnica do projeto e base para relatórios humanos posteriores.
    """
    try:
        prompt = f"""
        Você é um Principal Engineer e Arquiteto de Software revisando o histórico recente do projeto "{project_name}".
        Sua missão NÃO é apenas reescrever commits: você deve gerar To-Dos técnicos estruturados, ricos em contexto, úteis para o time interno e preparados para servir de base a relatórios futuros para clientes.

        ## TAREFAS JÁ EXISTENTES NESTE KANBAN:
        {existing_todos_text if existing_todos_text else "Ainda não há subtarefas registradas."}

        ## CONTEXTO DO REPOSITÓRIO / MÓDULOS MAIS QUENTES:
        {repo_context if repo_context else "Contexto agregado do repositório não informado."}

        ## HISTÓRICO DE COMMITS RECENTES PARA ANÁLISE:
        {commits_text}

        ## LOTE / FOCO DESTA GERAÇÃO:
        {batch_hint if batch_hint else 'Geração única sem particionamento explícito.'}

        ## OBJETIVO DA GERAÇÃO 2.3:
        Gere itens que representem o que foi feito, por que foi feito, em qual camada do sistema isso impacta, e como validar. O objetivo NÃO é comprimir um mês de trabalho em poucos épicos. Você deve preservar a sensação real de volume e complexidade do período, sem voltar ao ruído mecânico de 1 commit = 1 item sempre.

        ## REGRAS OBRIGATÓRIAS:
        1. NÃO invente funcionalidades. Baseie-se estritamente nos commits e no contexto do repositório.
        2. NÃO produza itens genéricos vazios. Cada item deve mencionar a intenção técnica da mudança.
        3. NÃO duplique itens já existentes no kanban se cobrirem o mesmo escopo.
        4. GRANULARIDADE OBRIGATÓRIA:
           - Para períodos grandes (ex.: 15 ou 30 dias), gere um volume robusto de itens. Como regra prática, você deve tender a produzir algo entre 60% e 95% do número de commits relevantes.
           - Para 30 dias, evite sair com menos de ~25 itens salvo se o histórico for realmente pequeno ou repetitivo demais.
           - AGRUPE apenas commits muito próximos e claramente da mesma microfrente técnica.
           - NÃO agrupe commits de naturezas diferentes (ex.: infra + frontend, parser + UI, backend + testes) num mesmo item.
           - Se houver uma sequência de refinamentos reais no mesmo módulo, gere múltiplos itens da mesma frente quando isso ajudar a refletir o volume real de trabalho.
           - Commits do mesmo tema, mas com objetivos diferentes (ex.: corrigir runtime, melhorar UX, refatorar onclick, carregar README, abrir modal, ajustar branch selector) DEVEM preferencialmente virar itens separados.
        5. REGRA DE ESTADO FINAL (CRÍTICA):
           - Quando houver commits conflitantes ou evolutivos na mesma área, o item deve refletir o ESTADO FINAL mais recente, e não uma média confusa do histórico.
           - Exemplo: se um commit adiciona Unix Socket e outro posterior desfaz isso para usar porta interna 5000, o To-Do deve descrever a decisão final adotada, mencionando no comentário que houve iteração/ajuste de abordagem.
        6. Sempre escreva o campo `texto` em linguagem técnica estruturada, começando obrigatoriamente por UMA destas categorias:
           - "**Análise**: ..."
           - "**Backend**: ..."
           - "**Frontend**: ..."
           - "**Feature**: ..."
           - "**Fix**: ..."
           - "**Melhorias**: ..."
           - "**Refactor**: ..."
           - "**Infraestrutura**: ..."
           - "**Verificação**: ..."
           - "**Sugestão**: ..."
           - "**Potencial futuro**: ..."
        7. O campo `texto` deve idealmente seguir esta lógica interna, mesmo que em uma linha só:
           categoria + ação + módulo/arquivos + objetivo/impacto.
           Exemplo bom:
           "**Backend**: Ajustar parser de `github_repo` em `routes.py` e fluxo de edição de projeto para suportar URLs com `.git` e evitar erro 404 na coleta de commits."
        8. O campo `comentario` deve ser mais rico do que antes. Inclua, quando possível:
           - commit/hash de origem (um ou mais)
           - autor real (nunca use placeholders como "Fulano" ou "autor desconhecido"; se faltar, use "Autor não identificado")
           - arquivos principais afetados
           - explicação curta do que aquilo desbloqueia, corrige ou melhora
           - se houver sequência de ajustes, deixe claro no comentário que foi uma evolução incremental
           - evite comentários vagos como "melhora a experiência do usuário" sem explicar tecnicamente o ganho
           - prefira comentários causais, no formato: "corrige X", "evita Y", "desbloqueia Z", "reduz risco de W", "garante consistência de K"
        9. O campo `completed` deve ser `true` para mudanças claramente já implementadas em commits fechados. Use `false` apenas se houver sinal explícito de WIP/incompleto.
        10. Gere também itens de camada superior quando o histórico apontar isso, por exemplo:
           - "**Análise**" para revisar consistência entre arquivos tocados várias vezes
           - "**Verificação**" para testes manuais/automatizados necessários
           - "**Sugestão**" para dívida técnica ou melhoria percebida a partir do padrão de commits
           - "**Potencial futuro**" para evolução plausível do módulo baseada no rumo recente do projeto
           Porém esses itens estratégicos NÃO devem substituir o detalhamento técnico principal; eles são complemento e devem representar no máximo 10% a 20% da saída total.
           Só gere "Sugestão" ou "Potencial futuro" se houver evidência concreta no histórico; caso contrário, prefira mais itens técnicos factuais.
           Só gere "Verificação" quando houver risco implícito claro, mudança visual relevante, migração sensível, fluxo novo ou sequência de correções que justificaria teste direcionado.
        11. O comentário deve soar como memória técnica do projeto, não apenas como “criado a partir do commit”.
        12. Priorize dar visibilidade ao volume de trabalho real do mês. Se houve muitas melhorias relevantes em uma mesma área, represente isso com mais de um item, desde que sem redundância textual.
        13. Se houver muitas frentes ativas no período, prefira errar por excesso controlado de itens técnicos do que por resumo excessivo.
        14. Não transforme a maior parte da saída em macro-resumos. A maior parte dos itens deve continuar sendo técnica, concreta e ancorada em commits/arquivos específicos.

        ## CRITÉRIO DE QUALIDADE:
        Uma saída excelente permite que alguém leia os To-Dos e entenda:
        - o que foi mexido no sistema
        - em que camada (backend/frontend/infra/etc.)
        - quais arquivos/módulos foram impactados
        - por que isso importa
        - o volume real do trabalho executado no período
        - o que ainda vale verificar ou evoluir

        ## FORMATO DE SAÍDA (JSON PURO):
        {{
          "todos": [
            {{
              "texto": "**Backend**: ...",
              "comentario": "Commits abc1234/def5678 por Fulano. Arquivos: routes.py, templates/kanban.html. Impacto: ...",
              "completed": true
            }}
          ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            return result.get('todos', [])
        return []
        
    except Exception as e:
        print(f"Erro ao gerar To-Dos via commits: {e}")
        return []

