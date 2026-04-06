import json
from datetime import datetime

from extensions import db
from models import UserIntegrationCredential


GOOGLE_CALENDAR_PROVIDER = 'google_calendar'
FIREFLIES_PROVIDER = 'fireflies'
MICROSOFT_PROVIDER = 'microsoft'


def get_user_integration(user_id, provider):
    return UserIntegrationCredential.query.filter_by(user_id=user_id, provider=provider).first()


def list_user_integrations(user_id):
    return UserIntegrationCredential.query.filter_by(user_id=user_id).order_by(UserIntegrationCredential.provider.asc()).all()


def get_user_integration_credentials(user_id, provider, default=None):
    record = get_user_integration(user_id, provider)
    if not record or not record.credentials_json:
        return default
    try:
        return json.loads(record.credentials_json)
    except Exception:
        return default


def upsert_user_integration(user_id, provider, credentials=None, account_email=None, enabled=True, meta=None):
    record = get_user_integration(user_id, provider)
    if not record:
        record = UserIntegrationCredential(user_id=user_id, provider=provider)
        db.session.add(record)

    if credentials is not None:
        record.credentials_json = json.dumps(credentials)
    if meta is not None:
        record.meta_json = json.dumps(meta)
    if account_email is not None:
        record.account_email = account_email

    record.is_enabled = enabled
    record.updated_at = datetime.utcnow()
    db.session.commit()
    return record


def disable_user_integration(user_id, provider):
    record = get_user_integration(user_id, provider)
    if not record:
        return None
    record.is_enabled = False
    record.updated_at = datetime.utcnow()
    db.session.commit()
    return record


def mark_user_integration_sync(user_id, provider):
    record = get_user_integration(user_id, provider)
    if not record:
        return None
    record.last_sync_at = datetime.utcnow()
    record.updated_at = datetime.utcnow()
    db.session.commit()
    return record
