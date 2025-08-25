import json
import os
from openai import OpenAI
import httpx

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configurar timeout mais agressivo para evitar travamento
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=15.0,  # Timeout de 15 segundos
    max_retries=0,  # Sem retry para evitar timeout do worker
    http_client=httpx.Client(timeout=15.0)
)

def process_project_transcription(transcription):
    """
    Processa a transcrição do projeto usando GPT-5 para preencher os campos estruturados
    """
    try:
        # Limitar transcrição para resposta mais rápida
        limited_transcription = transcription[:1500] if len(transcription) > 1500 else transcription
        
        prompt = f"""
        Extraia informações desta transcrição em JSON:

        {limited_transcription}

        Formato:
        {{
            "contexto_justificativa": "contexto breve",
            "descricao_resumida": "resumo em 1-2 linhas",
            "problema_oportunidade": "problema principal",
            "objetivos": "objetivos principais",
            "alinhamento_estrategico": "alinhamento estratégico",
            "escopo_projeto": "escopo principal",
            "fora_escopo": "fora do escopo",
            "premissas": "premissas principais",
            "restricoes": "restrições principais"
        }}

        Seja conciso.
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
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
        # Limitar transcrição para resposta mais rápida
        limited_transcription = transcription[:1000] if len(transcription) > 1000 else transcription
        
        prompt = f"""
        Gere 3-5 tarefas do projeto "{project_name}":

        {limited_transcription}

        JSON:
        {{
            "tasks": [
                {{"titulo": "tarefa 1", "descricao": "descrição breve"}},
                {{"titulo": "tarefa 2", "descricao": "descrição breve"}}
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-5",
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
