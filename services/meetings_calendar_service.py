import json
import logging
import os
import time
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from services.meeting_integrations_service import (
    GOOGLE_CALENDAR_PROVIDER,
    get_shared_integration,
    get_shared_integration_credentials,
    get_user_integration_credentials,
    upsert_user_integration,
    disable_user_integration,
)

logger = logging.getLogger(__name__)

GOOGLE_SCOPES = [
    'openid',
    'email',
    'profile',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]


def get_google_redirect_uri():
    env_redirect = os.environ.get('REDIRECT_URI')
    if env_redirect:
        return env_redirect
    return 'http://localhost/settings/google_callback'


def create_google_oauth_flow():
    client_id = (os.environ.get('GOOGLE_OAUTH_CLIENT_ID') or '').strip()
    client_secret = (os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET') or '').strip()
    redirect_uri = get_google_redirect_uri()

    if not client_id or not client_secret:
        raise ValueError('GOOGLE_OAUTH_CLIENT_ID ou GOOGLE_OAUTH_CLIENT_SECRET ausente')

    return Flow.from_client_config(
        {
            'web': {
                'client_id': client_id,
                'client_secret': client_secret,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
                'redirect_uris': [redirect_uri],
            }
        },
        scopes=GOOGLE_SCOPES,
        redirect_uri=redirect_uri,
    )


def get_google_authorization_url():
    flow = create_google_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return authorization_url, state


def exchange_google_code_for_credentials(code):
    client_id = (os.environ.get('GOOGLE_OAUTH_CLIENT_ID') or '').strip()
    client_secret = (os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET') or '').strip()
    redirect_uri = get_google_redirect_uri()

    from oauthlib.oauth2 import WebApplicationClient
    from requests_oauthlib import OAuth2Session

    client = WebApplicationClient(client_id)
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, client=client)
    token = oauth.fetch_token(
        'https://oauth2.googleapis.com/token',
        code=code,
        client_secret=client_secret
    )

    scope = token.get('scope', '')
    scopes = scope.split() if isinstance(scope, str) else scope

    credentials = Credentials(
        token=token.get('access_token'),
        refresh_token=token.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )

    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': credentials.expiry.isoformat() if credentials.expiry else None,
    }


def save_google_credentials_for_user(user_id, credentials, account_email=None):
    return upsert_user_integration(
        user_id=user_id,
        provider=GOOGLE_CALENDAR_PROVIDER,
        credentials=credentials,
        account_email=account_email,
        enabled=True,
    )


def disconnect_google_credentials_for_user(user_id):
    return disable_user_integration(user_id, GOOGLE_CALENDAR_PROVIDER)


def get_google_credentials_for_user(user_id):
    return get_user_integration_credentials(user_id, GOOGLE_CALENDAR_PROVIDER)


def get_shared_google_calendar_integration():
    return get_shared_integration(GOOGLE_CALENDAR_PROVIDER)


def get_shared_google_credentials():
    return get_shared_integration_credentials(GOOGLE_CALENDAR_PROVIDER)


def build_google_calendar_service(credentials_data):
    if not credentials_data:
        raise ValueError('Credenciais Google Calendar não encontradas para o usuário')

    expiry = None
    if credentials_data.get('expiry'):
        expiry = datetime.fromisoformat(credentials_data['expiry'])

    credentials = Credentials(
        token=credentials_data['token'],
        refresh_token=credentials_data.get('refresh_token'),
        token_uri=credentials_data['token_uri'],
        client_id=credentials_data['client_id'],
        client_secret=credentials_data['client_secret'],
        scopes=credentials_data['scopes'],
        expiry=expiry,
    )

    if credentials.expired and credentials.refresh_token:
        from google.auth.transport.requests import Request
        credentials.refresh(Request())

    return build('calendar', 'v3', credentials=credentials)


def list_google_calendar_events(service, max_results=20, include_recent=True):
    now = datetime.utcnow()
    time_min = (now - timedelta(days=7)).isoformat() + 'Z' if include_recent else now.isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime',
        timeZone='America/Sao_Paulo'
    ).execute()
    return events_result.get('items', [])


def create_google_calendar_event(service, title, description, start_time, end_time, attendees=None, recurrence=None):
    event = {
        'summary': title,
        'description': description,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        'conferenceData': {
            'createRequest': {
                'requestId': f'meeting-{int(time.time())}',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]

    if recurrence:
        rule = _build_rrule(recurrence)
        if rule:
            event['recurrence'] = [rule]

    created = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()
    return created


def get_google_calendar_event(service, event_id):
    return service.events().get(calendarId='primary', eventId=event_id, timeZone='America/Sao_Paulo').execute()


def _build_rrule(recurrence):
    if not recurrence:
        return None
    freq = recurrence.get('type', 'DAILY').upper()
    interval = recurrence.get('interval', 1)
    count = recurrence.get('count')
    weekdays = recurrence.get('weekdays', [])

    rule = f'RRULE:FREQ={freq};INTERVAL={interval}'
    if weekdays:
        rule += f";BYDAY={','.join(weekdays)}"
    if count and count != 'unlimited':
        rule += f';COUNT={count}'
    return rule
