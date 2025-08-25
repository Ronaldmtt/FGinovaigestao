import json
import os
from openai import OpenAI
import httpx

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configurar timeout extenso para processamento completo
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=60.0,  # Timeout de 60 segundos para processamento completo
    max_retries=0,  # Sem retry para evitar timeout do worker
    http_client=httpx.Client(timeout=60.0)
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
        Você é Sarah Chen, Senior Project Manager certificada PMP com 15 anos liderando projetos complexos em tecnologia, consultoria e inovação. Sua expertise inclui metodologias ágeis, gestão de stakeholders e transformação digital.

        MISSÃO: Analise esta transcrição como se fosse uma reunião do SEU projeto. Extraia cada ação, insight e oportunidade, transformando-os em um roadmap detalhado de tarefas executáveis.

        TRANSCRIÇÃO DA REUNIÃO DO PROJETO "{project_name}":
        {transcription}

        METODOLOGIA DE ANÁLISE (execute sequencialmente):

        FASE 1 - MAPEAMENTO COMPLETO:
        • Leia palavra por palavra, identificando: verbos de ação, substantivos-chave, pessoas mencionadas, prazos citados
        • Marque mentalmente: decisões tomadas, problemas levantados, soluções propostas, recursos discutidos
        • Identifique padrões: temas recorrentes, prioridades enfatizadas, urgências implícitas

        FASE 2 - CATEGORIZAÇÃO ESTRATÉGICA:
        • IMEDIATAS: Ações que precisam começar esta semana
        • PREPARATÓRIAS: Atividades necessárias antes de outras tarefas  
        • CORE: Entregas principais do projeto
        • VALIDAÇÃO: Aprovações, testes, confirmações necessárias
        • COMUNICAÇÃO: Alinhamentos, relatórios, apresentações
        • MITIGAÇÃO: Ações para resolver riscos ou obstáculos mencionados

        FASE 3 - DETALHAMENTO EXECUTIVO:
        Para cada tarefa identificada, defina:
        • CONTEXTO: Por que esta tarefa surgiu na discussão?
        • OBJETIVO: Resultado específico e mensurável esperado
        • METODOLOGIA: Como executar (ferramentas, processos, abordagem)
        • STAKEHOLDERS: Quem envolver (decisores, executores, consultados)
        • RECURSOS: Orçamento, tempo, ferramentas, informações necessárias
        • CRITÉRIOS DE SUCESSO: Como saber que foi bem executada
        • DEPENDÊNCIAS: O que precisa acontecer antes/depois
        • RISCOS: Obstáculos potenciais identificados na discussão

        CRITÉRIOS DE QUALIDADE PARA CADA TAREFA:
        ✓ Título: Verbo + objeto + contexto específico
        ✓ Descrição: Mínimo 5 frases cobrindo todos os 8 elementos acima
        ✓ Acionável: Qualquer PM conseguiria executar com essas informações
        ✓ Rastreável: Progresso pode ser medido objetivamente
        ✓ Contextualizada: Conecta claramente com a discussão da reunião

        EXEMPLO DE TAREFA DE ALTA QUALIDADE:
        {{
            "titulo": "Conduzir pesquisa de viabilidade técnica para integração com sistema legado",
            "descricao": "Com base na preocupação levantada sobre compatibilidade de sistemas, realizar análise técnica completa da integração proposta. Objetivos: identificar gaps técnicos, estimar esforço de desenvolvimento e propor arquitetura de solução. Metodologia: auditoria do sistema atual, prototipagem de conectores API, benchmarking de ferramentas similares. Envolver: arquiteto de sistemas (decisor), desenvolvedores senior (executores), fornecedor do sistema legado (consulta). Recursos necessários: acesso aos ambientes, documentação técnica atualizada, 40h de desenvolvimento. Critério de sucesso: relatório técnico com recomendação fundamentada e cronograma detalhado. Dependências: aguarda liberação de acesso pelo time de infraestrutura mencionada na reunião. Risco identificado: possível obsolescência das APIs conforme discussão sobre atualizações pendentes."
        }}

        FORMATO DE RESPOSTA - JSON estruturado:
        {{
            "tasks": [
                // Gere 12-25 tarefas seguindo rigorosamente os critérios de qualidade acima
                {{
                    "titulo": "Título executivo e específico",
                    "descricao": "Descrição completa seguindo os 8 elementos obrigatórios: contexto da discussão + objetivo mensurável + metodologia de execução + stakeholders envolvidos + recursos necessários + critérios de sucesso + dependências + riscos/obstáculos. Cada tarefa deve ser auto-suficiente para execução."
                }}
            ]
        }}

        DIRETRIZES FINAIS:
        • Priorize tarefas mencionadas múltiplas vezes ou com urgência explícita
        • Transforme cada problema discutido em tarefa de solução  
        • Converta cada decisão tomada em tarefa de implementação
        • Inclua tarefas de comunicação para decisões importantes
        • Adicione validações para entregas críticas mencionadas
        • Considere o ciclo completo: planejamento → execução → validação → comunicação

        Execute sua análise como a expert que você é. Cada tarefa deve refletir sua experiência em transformar discussões em execução estruturada.
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
