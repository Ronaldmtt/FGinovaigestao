import json
import os
import tempfile
from openai import OpenAI
import httpx

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=120.0,
    max_retries=0,
    http_client=httpx.Client(timeout=120.0)
)

MEETING_MODEL = "gpt-4o"
WHISPER_MODEL = "whisper-1"


def detect_meeting_language(text):
    try:
        response = client.chat.completions.create(
            model=MEETING_MODEL,
            messages=[
                {"role": "system", "content": "Detecte o idioma do texto. Responda apenas com o código do idioma, como pt, en, es."},
                {"role": "user", "content": text[:500]}
            ],
            temperature=0.1,
            max_tokens=10
        )
        return (response.choices[0].message.content or 'pt').strip().lower()
    except Exception:
        return 'pt'


def transcribe_meeting_audio(audio_file, max_file_size_mb=20):
    temp_file_path = None
    try:
        if hasattr(audio_file, 'seek'):
            audio_file.seek(0)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            audio_data = audio_file.read()
            if not audio_data:
                raise ValueError('Arquivo de áudio vazio')

            max_bytes = max_file_size_mb * 1024 * 1024
            if len(audio_data) > max_bytes:
                audio_data = audio_data[:max_bytes]

            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        with open(temp_file_path, 'rb') as audio:
            response = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio
            )
        return response.text
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass


def analyze_meeting(agenda, transcription, language=None, max_transcription_length=7000):
    try:
        if not language or language == 'auto':
            language = detect_meeting_language(f"{agenda[:150]} {transcription[:250]}")

        original_length = len(transcription or '')
        if original_length > max_transcription_length:
            first_part = transcription[:max_transcription_length // 3]
            last_part = transcription[-(max_transcription_length // 3):]
            middle_length = max_transcription_length - len(first_part) - len(last_part) - 100
            middle_start = max((original_length - middle_length) // 2, 0)
            middle_part = transcription[middle_start:middle_start + middle_length]
            transcription = f"{first_part}\n\n[...trecho omitido para processamento...]\n\n{middle_part}\n\n[...trecho omitido para processamento...]\n\n{last_part}"

        system_message = f"""
        Você é um analista sênior de reuniões.
        Responda integralmente no idioma detectado ({language}).

        Retorne APENAS um JSON no formato:
        {{
            "agenda_items": [{{"item": "string", "addressed": true, "context": "string"}}],
            "unaddressed_items": [{{"item": "string", "recommendation": "string"}}],
            "additional_topics": ["string"],
            "meeting_summary": "string",
            "alignment_score": 0,
            "insights": ["string"],
            "next_steps": ["string"],
            "action_items": ["string"],
            "directions": ["string"],
            "language": "{language}"
        }}
        """

        user_message = f"""
        PAUTA:
        {agenda}

        TRANSCRIÇÃO:
        {transcription}

        Analise o quanto a reunião cobriu a pauta, o que foi decidido, os principais insights, próximos passos, itens de ação e direções estratégicas.
        """

        response = client.chat.completions.create(
            model=MEETING_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
            max_tokens=1800
        )
        results = json.loads(response.choices[0].message.content)
        if 'language' not in results:
            results['language'] = language
        return results
    except Exception as e:
        return {
            "agenda_items": [],
            "unaddressed_items": [],
            "additional_topics": [],
            "meeting_summary": f"Não foi possível concluir a análise da reunião: {e}",
            "alignment_score": 0,
            "insights": ["Ocorreu um erro ao processar a análise desta reunião."],
            "next_steps": ["Revisar a transcrição e tentar novamente."],
            "action_items": [],
            "directions": [],
            "language": language or 'pt',
            "error": str(e)
        }


def generate_meeting_agenda(topic, description, language='pt'):
    prompt = f"""
    Você é um especialista em preparação de reuniões executivas.
    Gere uma pauta clara, objetiva e bem estruturada em {language}.

    Tópico: {topic}
    Descrição/contexto: {description}

    Retorne APENAS um JSON no formato:
    {{
        "title": "Título sugerido para a reunião",
        "agenda": "Lista de tópicos da pauta em texto simples"
    }}
    """

    response = client.chat.completions.create(
        model=MEETING_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.4,
        max_tokens=800
    )
    return json.loads(response.choices[0].message.content)
