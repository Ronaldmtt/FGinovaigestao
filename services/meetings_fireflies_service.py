import os
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
    payload = resp.json()
    return payload.get('data', {}).get('transcripts', [])


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
        sentences { index speaker_name text }
        summary { overview bullets }
        action_items { text }
      }
    }
    """
    resp = requests.post(FIREFLIES_URL, json={
        'operationName': 'GetTranscript',
        'query': query,
        'variables': {'id': transcript_id}
    }, headers=_headers(), timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    return payload.get('data', {}).get('transcript')


def find_transcript_by_title_and_date(title, target_date, limit=50):
    transcripts = list_transcripts(limit=limit)
    normalized_title = (title or '').strip().lower()
    for item in transcripts:
        item_title = (item.get('title') or '').strip().lower()
        item_date = (item.get('date') or '')[:10]
        if item_title == normalized_title and item_date == target_date:
            return item
    return None
