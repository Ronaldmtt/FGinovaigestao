"""
FG Transcritor Service — Integração com a API de criação de reuniões e transcrições.
URL Base: https://inovaimeet.com
"""
import os
import requests

API_KEY = os.getenv("FGTRANSCRITOR_API_KEY", "fgtranscritorpass")
BASE_URL = os.getenv("FGTRANSCRITOR_BASE_URL", "https://inovaimeet.com")
HUB_EMAIL = os.getenv("FGTRANSCRITOR_HUB_EMAIL", "hub@inovailab.com")
AUTH_HEADER = os.getenv("FGTRANSCRITOR_AUTH_HEADER", "X-API-Key")


def criar_reuniao(titulo, descricao, inicio, fim, participantes):
    """
    Cria uma reunião no FG Transcritor.
    
    Args:
        titulo: str - Título da reunião
        descricao: str - Descrição/agenda
        inicio: str - Data e hora de início (ISO 8601: "2026-02-15T14:00:00")
        fim: str - Data e hora de término (ISO 8601: "2026-02-15T15:00:00")
        participantes: list[str] - Lista de emails dos participantes
    
    Returns:
        {"ok": True, "result": {...}} em caso de sucesso
        {"ok": False, "error": "..."} em caso de falha
    """
    url = f"{BASE_URL}/api/create_meeting"
    
    payload = {
        "user_email": HUB_EMAIL,
        "title": titulo,
        "description": descricao,
        "start_time": inicio,
        "end_time": fim,
        "attendees": participantes,
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                AUTH_HEADER: API_KEY,
            },
            timeout=20,
        )
        
        if response.status_code in (200, 201):
            print(f"[transcritor] Reunião criada: {titulo}")
            return {"ok": True, "result": response.json()}
        else:
            error_msg = f"Status {response.status_code}: {response.text[:200]}"
            print(f"[transcritor] Erro ao criar reunião: {error_msg}")
            return {"ok": False, "error": error_msg}
            
    except requests.RequestException as e:
        print(f"[transcritor] Erro de conexão: {e}")
        return {"ok": False, "error": str(e)}


def buscar_transcricao(titulo, data):
    """
    Busca a transcrição de uma reunião no FG Transcritor.
    
    Args:
        titulo: str - Título exato da reunião (case-sensitive)
        data: str - Data no formato "YYYY-MM-DD"
    
    Returns:
        {"ok": True, "text": "transcrição..."} se encontrou
        {"ok": False, "pending": True} se ainda processando
        {"ok": False, "error": "..."} se não encontrou
    """
    url = f"{BASE_URL}/api/get_transcript"
    
    try:
        response = requests.post(
            url,
            json={"title": titulo, "date": data},
            headers={
                "Content-Type": "application/json",
                AUTH_HEADER: API_KEY,
            },
            timeout=20,
        )
        
        if response.status_code == 200:
            result = response.json()
            text = result.get("transcription") or result.get("transcript") or result.get("text")
            if text:
                return {"ok": True, "text": text}
            return {"ok": False, "error": "Transcrição vazia"}
        
        if response.status_code in (202, 204):
            return {"ok": False, "pending": True, "message": "Transcrição ainda sendo processada"}
        
        return {"ok": False, "error": f"Status {response.status_code}: {response.text[:200]}"}
        
    except requests.RequestException as e:
        print(f"[transcritor] Erro ao buscar transcrição: {e}")
        return {"ok": False, "error": str(e)}
