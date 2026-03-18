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

def generate_project_report_summary(project_name, description, problem, objectives):
    """
    Gera um parágrafo de síntese profissional para relatório com base nos campos do projeto.
    """
    try:
        prompt = f"""
        Atue como um Arquiteto de Software e Gerente de Projetos Especialista com acesso total ao código fonte deste projeto.

        Sua tarefa é analisar profundamente a estrutura de arquivos, o código backend (Python/Flask), o frontend (HTML/JS/Templates) e o banco de dados.
        Entenda a funcionalidade do sistema atual, os fluxos de usuário e as regras de negócio implementadas.

        Com base NESSA análise automática que você fará agora, gere um documento de documentação técnica em Markdown seguindo EXATAMENTE o modelo abaixo.
        Você não precisa inventar dados, use os dados reais extraídos do código e da estrutura do projeto.
        O resultado será salvo em um arquivo .md dentro da pasta raiz do projeto. Siga estritamente o que é pedido neste prompt.

        REGRAS OBRIGATÓRIAS DE FORMATAÇÃO (SIGA ESTRITAMENTE):
        - Você PODE e DEVE usar títulos com ### (três cerquilhas) para identificar as seções, pois o parser do sistema depende deles para encontrar o conteúdo.
        - NÃO crie subtítulos (####, #####) abaixo dos títulos ###. O conteúdo abaixo de cada ### deve ser apenas texto corrido.
        - NÃO use headers de nível 1 (#) ou nível 2 (##). Use APENAS ### para títulos de seção.
        - Se você criar subtítulos (#### ou mais), o sistema não conseguirá processar o conteúdo.

        Informações Base do Projeto "{project_name}":
        1. Descrição: {description}
        2. Problema/Oportunidade: {problem}
        3. Objetivos: {objectives}

        Os tópicos obrigatórios são:

        ### Descrição Resumida
        (Um resumo conciso do projeto baseado no que o código faz)

        ### Problema/Oportunidade
        (O problema que estamos resolvendo ou a oportunidade de negócio que o software ataca)

        ### Objetivos
        (Objetivos técnicos e funcionais do sistema)

        ### Alinhamento Estratégico
        (Como a arquitetura e tecnologias escolhidas suportam o crescimento do projeto)

        ### Escopo do Projeto
        (O que está implementado atualmente no código: Módulos, Funcionalidades, Integrações)

        ### Fora do Escopo
        (O que claramente não está implementado no código atual)

        ### Premissas
        (Premissas técnicas adotadas: Stack, Bibliotecas, Padrões)

        ### Restrições
        (Limitações técnicas ou de arquitetura encontradas na análise)

        ---
        Gere o conteúdo em Português do Brasil com base na sua análise do código.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        return content.strip()
        
    except Exception as e:
        print(f"Erro ao gerar resumo do projeto para relatório: {e}")
        # Fallback se a IA falhar: concatenação simples
        return f"{description}. O projeto visa resolver: {problem}. Principais objetivos: {objectives}."

def generate_client_report_from_tasks(project_name, tasks):
    """
    Gera um relatório executivo para clientes com base nas tarefas técnicas.
    Traduz 'tech-speak' para 'business-value'.
    
    tasks: lista de dicts {'titulo': str, 'descricao': str, 'status': str}
    """
    try:
        # Preparar lista de tarefas para o prompt
        tasks_text = ""
        for t in tasks:
            status_symbol = "✓" if t.get('status') == 'concluida' else "○"
            tasks_text += f"{status_symbol} [Status: {t.get('status')}] {t.get('titulo')}: {t.get('descricao')}\n"
            
        prompt = f"""
        Você é um Gerente de Contas Sênior reportando o progresso do projeto "{project_name}" para um cliente NÃO-TÉCNICO (CEO/Diretor de empresa).
        
        Sua missão: Traduzir a lista de tarefas técnicas abaixo em um relatório de progresso focado em VALOR DE NEGÓCIO.
        
        TAREFAS TÉCNICAS EXECUTADAS/EM ANDAMENTO:
        {tasks_text}
        
        DIRETRIZES:
        1. Ignore jargões técnicos (ex: "refatorar rota", "ajustar query SQL", "blueprints"). Substitua por termos de negócio (ex: "melhoria na estrutura do sistema", "otimização de banco de dados").
        2. Agrupe tarefas pequenas e relacionadas em um único ponto de progresso robusto.
        3. Enfatize o que já foi entregue (✓) e o que está em andamento (○).
        4. O tom deve ser profissional, confiante e transparente.
        
        Retorne APENAS um JSON no seguinte formato:
        {{
            "resumo_executivo": "Um parágrafo de 3-4 linhas resumindo o estado geral do projeto e as principais conquistas recentes.",
            "entregas_recentes": [
                "Ponto 1 (focado em valor)",
                "Ponto 2 (focado em valor)"
            ],
            "proximos_passos": [
                "O que será focado a seguir (traduzido para linguagem de negócio)"
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        return None
        
    except Exception as e:
        print(f"Erro ao gerar relatório de cliente: {e}")
        return None

def generate_kanban_todos_from_commits(commits_text, project_name, existing_todos_text="", repo_context=""):
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

        ## OBJETIVO DA GERAÇÃO 2.0:
        Gere itens que representem o que foi feito, por que foi feito, em qual camada do sistema isso impacta, e como validar. Os itens podem ser numerosos, desde que sejam úteis, técnicos e semanticamente corretos.

        ## REGRAS OBRIGATÓRIAS:
        1. NÃO invente funcionalidades. Baseie-se estritamente nos commits e no contexto do repositório.
        2. NÃO produza itens genéricos vazios. Cada item deve mencionar a intenção técnica da mudança.
        3. NÃO duplique itens já existentes no kanban se cobrirem o mesmo escopo.
        4. Você PODE manter granularidade alta, mas deve agrupar microcommits puramente cosméticos quando fizerem parte da mesma frente técnica.
        5. Sempre escreva o campo `texto` em linguagem técnica estruturada, começando obrigatoriamente por UMA destas categorias:
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
        6. O campo `texto` deve idealmente seguir esta lógica interna, mesmo que em uma linha só:
           categoria + ação + módulo/arquivos + objetivo/impacto.
           Exemplo bom:
           "**Backend**: Ajustar parser de `github_repo` em `routes.py` e fluxo de edição de projeto para suportar URLs com `.git` e evitar erro 404 na coleta de commits."
        7. O campo `comentario` deve ser mais rico do que antes. Inclua, quando possível:
           - commit/hash de origem
           - autor
           - arquivos principais afetados
           - explicação curta do que aquilo desbloqueia, corrige ou melhora
        8. O campo `completed` deve ser `true` para mudanças claramente já implementadas em commits fechados. Use `false` apenas se houver sinal explícito de WIP/incompleto.
        9. IMPORTANTE: Gere também itens de camada superior quando o histórico apontar isso, por exemplo:
           - "**Análise**" para revisar consistência entre arquivos tocados várias vezes
           - "**Verificação**" para testes manuais/automatizados necessários
           - "**Sugestão**" para dívida técnica ou melhoria percebida a partir do padrão de commits
           - "**Potencial futuro**" para evolução plausível do módulo baseada no rumo recente do projeto
        10. O comentário deve soar como memória técnica do projeto, não apenas como “criado a partir do commit”.

        ## CRITÉRIO DE QUALIDADE:
        Uma saída excelente permite que alguém leia os To-Dos e entenda:
        - o que foi mexido no sistema
        - em que camada (backend/frontend/infra/etc.)
        - quais arquivos/módulos foram impactados
        - por que isso importa
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

