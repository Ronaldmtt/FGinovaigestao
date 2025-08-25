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
        Você é um especialista em gestão de projetos com 15 anos de experiência. Analise minuciosamente esta transcrição de reunião sobre o projeto "{project_name}" e extraia TODAS as tarefas, atividades, ações e responsabilidades mencionadas ou implícitas na discussão.

        TRANSCRIÇÃO COMPLETA PARA ANÁLISE:
        {transcription}

        INSTRUÇÕES DETALHADAS PARA ANÁLISE PROFUNDA:
        1. Leia cuidadosamente TODA a transcrição palavra por palavra - não pule nenhuma seção
        2. Identifique TODAS as ações explícitas: tarefas, deliverables, pesquisas, reuniões, contatos, decisões mencionadas
        3. Identifique tarefas IMPLÍCITAS baseadas no contexto: preparação necessária, validações pendentes, follow-ups obrigatórios
        4. Para cada ponto discutido ou problema levantado, crie uma tarefa específica e acionável
        5. Inclua tarefas de diferentes fases: preparação, execução, validação, follow-up e documentação
        6. Seja extremamente específico sobre O QUE fazer, COMO fazer, QUEM envolver, RECURSOS necessários, CRITÉRIOS de sucesso
        7. Gere entre 10-20 tarefas detalhadas e abrangentes (extraia o máximo absoluto da transcrição)
        8. Priorize tarefas que foram mencionadas múltiplas vezes ou enfatizadas na discussão
        9. Considere dependências entre tarefas e crie etapas lógicas de execução

        FORMATO DE RESPOSTA - JSON com tarefas extremamente detalhadas:
        {{
            "tasks": [
                {{
                    "titulo": "Título claro, específico e acionável da tarefa",
                    "descricao": "Descrição completa e detalhada do que deve ser feito, incluindo: contexto completo da discussão, objetivos específicos e mensuráveis, recursos e ferramentas necessários, pessoas ou departamentos a serem envolvidos, critérios claros de sucesso, próximos passos detalhados, prazos sugeridos quando mencionados, e possíveis riscos ou obstáculos identificados na discussão. Mínimo de 4-6 frases explicativas e contextuais."
                }}
            ]
        }}

        ELEMENTOS CRÍTICOS PARA IDENTIFICAR NA TRANSCRIÇÃO:
        - Pesquisas de mercado, técnicas ou de viabilidade a serem realizadas
        - Contatos com clientes, fornecedores, parceiros ou stakeholders
        - Reuniões de planejamento, validação, apresentação ou follow-up a serem agendadas
        - Documentos técnicos, propostas, contratos ou relatórios a serem criados
        - Análises financeiras, técnicas, de risco ou de mercado a serem conduzidas
        - Decisões estratégicas, técnicas ou operacionais pendentes
        - Aprovações de orçamento, recursos, cronograma ou escopo necessárias
        - Testes, protótipos, validações ou provas de conceito a serem executados
        - Validações com usuários finais, clientes ou stakeholders internos
        - Preparação de apresentações, demos ou materiais de comunicação
        - Levantamento de requisitos funcionais, técnicos ou de negócio
        - Definição de processos, metodologias ou fluxos de trabalho
        - Treinamentos, capacitações ou transferência de conhecimento
        - Monitoramento, acompanhamento ou controle de progresso
        - Comunicação com equipes, gerência ou partes interessadas

        CONTEXTO ADICIONAL PARA CONSIDERAR:
        - Se algo foi mencionado como "importante", "urgente" ou "crítico", crie tarefas detalhadas para isso
        - Se houve discussão sobre problemas ou desafios, crie tarefas para solucioná-los
        - Se foram mencionados prazos ou marcos, incorpore isso nas descrições das tarefas
        - Se houve debate sobre diferentes abordagens, crie tarefas para avaliar as opções
        - Se foram identificados riscos ou dependências, crie tarefas para mitigá-los

        Sua missão é extrair o máximo valor possível desta transcrição, transformando cada insight, discussão e ponto levantado em tarefas acionáveis e bem estruturadas. Responda APENAS com o JSON das tarefas detalhadas.
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
