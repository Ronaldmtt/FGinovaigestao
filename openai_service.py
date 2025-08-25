import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def process_project_transcription(transcription):
    """
    Processa a transcrição do projeto usando GPT-5 para preencher os campos estruturados
    """
    try:
        prompt = f"""
        Com base na seguinte transcrição de projeto, preencha os campos abaixo de forma estruturada e detalhada:

        Transcrição: {transcription}

        Por favor, forneça as informações no seguinte formato JSON:
        {{
            "contexto_justificativa": "descrição do contexto e justificativa",
            "descricao_resumida": "descrição resumida do projeto",
            "problema_oportunidade": "problema ou oportunidade que o projeto resolve",
            "objetivos": "objetivos gerais e específicos",
            "alinhamento_estrategico": "como se conecta à estratégia da empresa",
            "escopo_projeto": "o que será entregue",
            "fora_escopo": "o que NÃO será feito",
            "premissas": "premissas do projeto",
            "restricoes": "restrições do projeto"
        }}

        Seja específico e detalhado em cada campo. Se alguma informação não estiver clara na transcrição, faça inferências razoáveis baseadas no contexto.
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
        prompt = f"""
        Com base na seguinte transcrição sobre o projeto "{project_name}", gere uma lista de tarefas específicas e acionáveis:

        Transcrição: {transcription}

        Por favor, forneça as tarefas no seguinte formato JSON:
        {{
            "tasks": [
                {{
                    "titulo": "título da tarefa",
                    "descricao": "descrição detalhada da tarefa"
                }},
                {{
                    "titulo": "título da tarefa 2",
                    "descricao": "descrição detalhada da tarefa 2"
                }}
            ]
        }}

        Gere entre 3 a 8 tarefas. Cada tarefa deve ser específica, acionável e ter um título claro.
        As descrições devem incluir o que precisa ser feito e, se aplicável, critérios de aceitação.
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
