import os
from datetime import datetime, timezone
import requests

FIREFLIES_URL = 'https://api.fireflies.ai/graphql'


def _headers():
    token = os.environ.get('FIREFLIES_API_TOKEN')
    if not token:
        raise ValueError('FIREFLIES_API_TOKEN não configurado')
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }


def list_transcripts(limit=50):
    query = """
    query ListTranscripts($limit: Int) {
      transcripts(limit: $limit) {
        id
        title
        date
        meeting_link
      }
    }
    """
    resp = requests.post(FIREFLIES_URL, json={
        'operationName': 'ListTranscripts',
        'query': query,
        'variables': {'limit': limit}
    }, headers=_headers(), timeout=30)
    resp.raise_for_status()
    payload = resp.json() or {}
    data = payload.get('data') or {}
    transcripts = data.get('transcripts') or []
    if not isinstance(transcripts, list):
        return []
    return [item for item in transcripts if isinstance(item, dict)]


def get_transcript(transcript_id):
    query = """
    query GetTranscript($id:String!){
      transcript(id:$id){
        id
        title
        date
        transcript_url
        audio_url
        video_url
        meeting_link
        duration
        speakers { id name }
        sentences { index speaker_name text start_time end_time }
        summary { overview bullet_gist }
      }
    }
    """
    resp = requests.post(FIREFLIES_URL, json={
        'operationName': 'GetTranscript',
        'query': query,
        'variables': {'id': transcript_id}
    }, headers=_headers(), timeout=30)
    resp.raise_for_status()
    payload = resp.json() or {}
    if payload.get('errors'):
        messages = '; '.join((item.get('message') or 'Fireflies GraphQL error') for item in (payload.get('errors') or []) if isinstance(item, dict))
        raise ValueError(messages or 'Fireflies GraphQL error')
    return (payload.get('data') or {}).get('transcript')


def _normalize_fireflies_date(item_date):
    if item_date in (None, ''):
        return None
    if isinstance(item_date, (int, float)):
        return datetime.fromtimestamp(item_date / 1000, tz=timezone.utc).date().isoformat()
    item_date = str(item_date).strip()
    if len(item_date) >= 10 and item_date[4] == '-' and item_date[7] == '-':
        return item_date[:10]
    if item_date.isdigit():
        return datetime.fromtimestamp(int(item_date) / 1000, tz=timezone.utc).date().isoformat()
    return item_date[:10]


def find_transcript_by_title_and_date(title, target_date, limit=50):
    transcripts = list_transcripts(limit=limit) or []
    normalized_title = (title or '').strip().lower()
    target_date = (target_date or '').strip()[:10]
    for item in transcripts:
        if not isinstance(item, dict):
            continue
        item_title = (item.get('title') or '').strip().lower()
        item_date = _normalize_fireflies_date(item.get('date'))
        if item_title == normalized_title and item_date == target_date:
            return item
    return None
