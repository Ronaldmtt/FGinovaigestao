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
        # Limitar transcrição drasticamente para resposta mais rápida
        limited_transcription = transcription[:800] if len(transcription) > 800 else transcription
        
        prompt = f"""
        Extraia dados desta transcrição e retorne em formato JSON:
        {limited_transcription}

        Retorne um JSON com estes campos:
        {{
            "contexto_justificativa": "texto",
            "descricao_resumida": "texto",
            "problema_oportunidade": "texto",
            "objetivos": "texto",
            "alinhamento_estrategico": "texto",
            "escopo_projeto": "texto",
            "fora_escopo": "texto",
            "premissas": "texto",
            "restricoes": "texto"
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
        # Limitar transcrição drasticamente para resposta mais rápida
        limited_transcription = transcription[:500] if len(transcription) > 500 else transcription
        
        prompt = f"""
        Gere 3 tarefas para: {project_name}
        {limited_transcription}

        Retorne um JSON com este formato:
        {{
            "tasks": [
                {{"titulo": "texto", "descricao": "texto"}},
                {{"titulo": "texto", "descricao": "texto"}},
                {{"titulo": "texto", "descricao": "texto"}}
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
