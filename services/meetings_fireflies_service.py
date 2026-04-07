import os
import re
import unicodedata
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


def _normalize_text(value):
    value = '' if value is None else str(value)
    value = unicodedata.normalize('NFKC', value)
    value = ''.join(ch for ch in value if not unicodedata.category(ch).startswith('C'))
    value = re.sub(r'\s+', ' ', value).strip().lower()
    return value


def _normalize_meeting_link(link):
    link = _normalize_text(link)
    if not link:
        return ''
    link = link.replace('http://', 'https://')
    if link.endswith('/'):
        link = link[:-1]
    return link


def _extract_google_meet_code(link):
    normalized = _normalize_meeting_link(link)
    if not normalized:
        return ''
    match = re.search(r'meet\.google\.com/([a-z]{3}-[a-z]{4}-[a-z]{3})', normalized)
    return (match.group(1) if match else '').strip().lower()


def match_transcript_from_list(transcripts, meeting_link=None, title=None, target_date=None):
    transcripts = transcripts or []
    normalized_link = _normalize_meeting_link(meeting_link)
    meet_code = _extract_google_meet_code(meeting_link)
    normalized_title = _normalize_text(title)
    normalized_date = (target_date or '').strip()[:10]

    for item in transcripts:
        if not isinstance(item, dict):
            continue
        item_link_raw = item.get('meeting_link')
        item_link = _normalize_meeting_link(item_link_raw)
        item_code = _extract_google_meet_code(item_link_raw)
        if normalized_link and item_link and (item_link == normalized_link or normalized_link in item_link or item_link in normalized_link):
            return item, 'meeting_link'
        if meet_code and item_code and (item_code == meet_code or meet_code in item_code or item_code in meet_code):
            return item, 'meet_code'

    for item in transcripts:
        if not isinstance(item, dict):
            continue
        item_title = _normalize_text(item.get('title'))
        item_date = _normalize_fireflies_date(item.get('date'))
        if normalized_title and normalized_date and item_title == normalized_title and item_date == normalized_date:
            return item, 'title_date'

    return None, None


def find_transcript_by_meeting_link(meeting_link, limit=100):
    transcripts = list_transcripts(limit=limit) or []
    match, _strategy = match_transcript_from_list(transcripts, meeting_link=meeting_link)
    return match


def find_transcript_by_title_and_date(title, target_date, limit=50):
    transcripts = list_transcripts(limit=limit) or []
    match, _strategy = match_transcript_from_list(transcripts, title=title, target_date=target_date)
    return match


def summarize_recent_transcripts(limit=5):
    transcripts = list_transcripts(limit=max(limit, 1)) or []
    summary = []
    for item in transcripts[:limit]:
        if not isinstance(item, dict):
            continue
        summary.append({
            'id': item.get('id'),
            'title': item.get('title'),
            'date': _normalize_fireflies_date(item.get('date')),
            'meeting_link': item.get('meeting_link'),
            'meet_code': _extract_google_meet_code(item.get('meeting_link')),
        })
    return summary
