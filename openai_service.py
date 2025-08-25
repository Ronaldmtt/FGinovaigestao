import json
import os
from openai import OpenAI
import httpx

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configurar timeout balanceado
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=20.0,  # Timeout de 20 segundos para processar mais contexto
    max_retries=0,  # Sem retry para evitar timeout do worker
    http_client=httpx.Client(timeout=20.0)
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
        Você é um especialista em gestão de projetos. Analise esta transcrição de reunião sobre o projeto "{project_name}" e extraia TODAS as tarefas, atividades, ações e responsabilidades mencionadas ou implícitas na discussão.

        TRANSCRIÇÃO COMPLETA:
        {transcription}

        INSTRUÇÕES DETALHADAS:
        1. Leia cuidadosamente TODA a transcrição - não pule nenhuma parte
        2. Identifique TODAS as ações, tarefas, deliverables, pesquisas, reuniões, contatos, decisões mencionadas
        3. Identifique também tarefas IMPLÍCITAS baseadas no contexto da discussão
        4. Para cada ponto discutido, crie uma tarefa específica e acionável
        5. Inclua tarefas de preparação, execução, follow-up e validação quando relevante
        6. Seja específico sobre o QUE fazer, COMO fazer, QUEM envolver, RECURSOS necessários
        7. Gere entre 8-15 tarefas detalhadas (extraia o máximo da transcrição)
        8. Priorize tarefas que foram mencionadas MÚLTIPLAS VEZES na discussão

        FORMATO DE RESPOSTA - JSON com tarefas detalhadas:
        {{
            "tasks": [
                {{
                    "titulo": "Título claro e específico da tarefa",
                    "descricao": "Descrição completa e detalhada do que deve ser feito, incluindo contexto da discussão, objetivos específicos, recursos necessários, critérios de sucesso e próximos passos. Mínimo 2-3 frases explicativas."
                }}
            ]
        }}

        EXEMPLOS do que procurar na transcrição:
        - Pesquisas a serem realizadas
        - Contatos a serem feitos
        - Reuniões a serem agendadas
        - Documentos a serem criados
        - Análises a serem conduzidas
        - Decisões pendentes
        - Aprovações necessárias
        - Testes a serem executados
        - Validações com stakeholders
        - Preparação de apresentações
        - Levantamento de requisitos
        - Definição de processos

        Responda APENAS com o JSON das tarefas, extraindo o máximo de valor da transcrição fornecida.
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
