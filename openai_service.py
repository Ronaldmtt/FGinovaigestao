import json
import os
from openai import OpenAI
import httpx

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configurar timeout muito agressivo para evitar travamento
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=10.0,  # Timeout de 10 segundos
    max_retries=0,  # Sem retry para evitar timeout do worker
    http_client=httpx.Client(timeout=10.0)
)

def process_project_transcription(transcription):
    """
    Processa a transcrição do projeto usando GPT-5 para preencher os campos estruturados
    """
    try:
        # Limitar transcrição para balancear contexto e velocidade
        limited_transcription = transcription[:2500] if len(transcription) > 2500 else transcription
        
        prompt = f"""
        Analise esta transcrição de reunião/projeto e extraia informações relevantes em formato JSON:

        {limited_transcription}

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
        # Limitar transcrição para balancear contexto e velocidade  
        limited_transcription = transcription[:2000] if len(transcription) > 2000 else transcription
        
        prompt = f"""
        Com base nesta transcrição de reunião sobre o projeto "{project_name}", gere tarefas específicas em formato JSON:

        {limited_transcription}

        Analise o conteúdo da transcrição e crie 3-5 tarefas práticas e relevantes ao que foi discutido:
        {{
            "tasks": [
                {{"titulo": "título da tarefa baseado na discussão", "descricao": "descrição específica do que fazer"}},
                {{"titulo": "título da tarefa baseado na discussão", "descricao": "descrição específica do que fazer"}},
                {{"titulo": "título da tarefa baseado na discussão", "descricao": "descrição específica do que fazer"}}
            ]
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
            return result.get('tasks', [])
        return []
        
    except Exception as e:
        print(f"Erro ao gerar tarefas da transcrição: {e}")
        return []
