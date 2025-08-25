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
        ✓ Título Executivo: Verbo de ação + objeto específico + contexto detalhado do projeto
        ✓ Descrição Profissional: Mínimo 6-8 frases cobrindo obrigatoriamente todos os 8 elementos detalhados acima
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
                    "titulo": "Título executivo, específico e completamente acionável",
                    "descricao": "Descrição executiva e completa seguindo obrigatoriamente os 8 elementos detalhados: contexto completo da discussão + objetivo mensurável específico + metodologia detalhada de execução + stakeholders mapeados e seus papéis + recursos necessários especificados + critérios objetivos de sucesso + dependências mapeadas + riscos e obstáculos identificados. Cada tarefa deve ser completamente auto-suficiente para execução imediata por qualquer gerente de projetos experiente."
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
