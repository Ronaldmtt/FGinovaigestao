#!/usr/bin/env python3
"""
Importa dados do projeto daniel-fgtranscritor para o banco do FGinovaigestao.

Uso esperado (exemplo):
    python scripts/import_transcritor_data.py \
        --source-url "$TRANSCRITOR_DATABASE_URL" \
        --dry-run

Premissas:
- banco de destino = banco do Gestão (carregado pelo app Flask local)
- reconciliação de usuários por email
- sem criar auth próprio do Transcritor
- foca inicialmente em reuniões + integrações Google
"""

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, text

from app import app
from extensions import db
from models import Meeting, User
from services.meeting_integrations_service import GOOGLE_CALENDAR_PROVIDER, get_user_integration, upsert_user_integration


def parse_args():
    parser = argparse.ArgumentParser(description='Importar dados do Transcritor para o Gestão')
    parser.add_argument('--source-url', required=True, help='SQLALCHEMY URL do banco do Transcritor')
    parser.add_argument('--dry-run', action='store_true', help='Somente simular, sem gravar no banco do Gestão')
    parser.add_argument('--limit', type=int, default=0, help='Limite opcional de reuniões para teste')
    parser.add_argument('--report-json', default='transcritor_import_report.json', help='Caminho do relatório JSON de auditoria')
    return parser.parse_args()


def fetch_source_users(conn):
    rows = conn.execute(text("""
        SELECT id, email, username, google_credentials, google_calendar_enabled
        FROM "user"
        ORDER BY id
    """)).mappings().all()
    return list(rows)


def fetch_source_meetings(conn, limit=0):
    sql = """
        SELECT id, title, agenda, transcription, language, alignment_score,
               meeting_date, created_at, user_id, results_json,
               audio_url, video_url, google_calendar_event_id,
               fireflies_transcript_id
        FROM meeting
        ORDER BY created_at ASC, id ASC
    """
    if limit and limit > 0:
        sql += f" LIMIT {int(limit)}"
    rows = conn.execute(text(sql)).mappings().all()
    return list(rows)


def normalize_dt(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    try:
        parsed = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except Exception:
        return None


def migrate_google_integrations(source_users, dry_run=False):
    report = Counter()
    issues = []
    email_to_target = {u.email.strip().lower(): u for u in User.query.filter(User.email.isnot(None)).all()}

    for source_user in source_users:
        email = (source_user.get('email') or '').strip().lower()
        if not email:
            report['users_without_email'] += 1
            issues.append({'type': 'user_without_email', 'source_user_id': source_user.get('id')})
            continue

        target_user = email_to_target.get(email)
        if not target_user:
            report['users_not_found_in_target'] += 1
            issues.append({'type': 'user_not_found_in_target', 'source_user_id': source_user.get('id'), 'email': email})
            continue

        credentials_raw = source_user.get('google_credentials')
        enabled = bool(source_user.get('google_calendar_enabled'))
        if not credentials_raw and not enabled:
            report['users_without_google_credentials'] += 1
            continue

        try:
            credentials = json.loads(credentials_raw) if credentials_raw else None
        except Exception:
            credentials = None
            issues.append({'type': 'invalid_google_credentials_json', 'source_user_id': source_user.get('id'), 'email': email})

        if dry_run:
            report['google_integrations_would_upsert'] += 1
            continue

        existing = get_user_integration(target_user.id, GOOGLE_CALENDAR_PROVIDER)
        if existing and existing.credentials_json:
            report['google_integrations_already_present'] += 1
            continue

        upsert_user_integration(
            user_id=target_user.id,
            provider=GOOGLE_CALENDAR_PROVIDER,
            credentials=credentials,
            account_email=target_user.email,
            enabled=enabled,
            meta={'imported_from': 'daniel-fgtranscritor'}
        )
        report['google_integrations_imported'] += 1

    return report, issues


def migrate_meetings(source_meetings, source_users, dry_run=False):
    report = Counter()
    issues = []
    source_user_by_id = {row['id']: row for row in source_users}
    email_to_target = {u.email.strip().lower(): u for u in User.query.filter(User.email.isnot(None)).all()}

    for source_meeting in source_meetings:
        source_user = source_user_by_id.get(source_meeting.get('user_id'))
        if not source_user:
            report['meetings_missing_source_user'] += 1
            issues.append({'type': 'meeting_missing_source_user', 'source_meeting_id': source_meeting.get('id')})
            continue

        email = (source_user.get('email') or '').strip().lower()
        target_user = email_to_target.get(email)
        if not target_user:
            report['meetings_user_not_found_in_target'] += 1
            issues.append({'type': 'meeting_user_not_found_in_target', 'source_meeting_id': source_meeting.get('id'), 'email': email})
            continue

        title = (source_meeting.get('title') or '').strip() or f"Reunião importada {source_meeting.get('id')}"
        google_event_id = source_meeting.get('google_calendar_event_id')
        fireflies_id = source_meeting.get('fireflies_transcript_id')

        duplicate = None
        if google_event_id:
            duplicate = Meeting.query.filter_by(google_calendar_event_id=google_event_id).first()
        if not duplicate:
            duplicate = Meeting.query.filter_by(
                title=title,
                created_by_id=target_user.id,
                fireflies_transcript_id=fireflies_id
            ).first() if fireflies_id else None

        if duplicate:
            report['meetings_already_present'] += 1
            issues.append({'type': 'meeting_duplicate_detected', 'source_meeting_id': source_meeting.get('id'), 'duplicate_target_meeting_id': duplicate.id, 'title': title})
            continue

        payload = {
            'source_meeting_id': source_meeting.get('id'),
            'source_user_email': email,
            'imported_from': 'daniel-fgtranscritor'
        }

        meeting = Meeting(
            title=title,
            date_time=normalize_dt(source_meeting.get('meeting_date')) or normalize_dt(source_meeting.get('created_at')) or datetime.utcnow(),
            agenda=source_meeting.get('agenda'),
            transcription_content=source_meeting.get('transcription'),
            language=source_meeting.get('language'),
            alignment_score=source_meeting.get('alignment_score'),
            results_json=source_meeting.get('results_json'),
            audio_url=source_meeting.get('audio_url'),
            video_url=source_meeting.get('video_url'),
            google_calendar_event_id=google_event_id,
            fireflies_transcript_id=fireflies_id,
            meeting_source='transcritor_import',
            analysis_status='completed' if source_meeting.get('results_json') else 'pending',
            analysis_generated_at=normalize_dt(source_meeting.get('created_at')),
            meeting_owner_email=email,
            raw_provider_payload=json.dumps(payload),
            created_by_id=target_user.id,
            status='concluida' if source_meeting.get('results_json') else 'agendada',
        )

        try:
            results = json.loads(source_meeting.get('results_json')) if source_meeting.get('results_json') else {}
        except Exception:
            results = {}
            issues.append({'type': 'meeting_invalid_results_json', 'source_meeting_id': source_meeting.get('id'), 'title': title})
        meeting.analysis_summary = (results or {}).get('meeting_summary')

        if dry_run:
            report['meetings_would_import'] += 1
            continue

        db.session.add(meeting)
        db.session.flush()
        if target_user not in meeting.participants:
            meeting.participants.append(target_user)
        report['meetings_imported'] += 1

    if not dry_run:
        db.session.commit()

    return report, issues


def print_report(title, report):
    print(f"\n=== {title} ===")
    if not report:
        print('Sem itens.')
        return
    for key in sorted(report.keys()):
        print(f"- {key}: {report[key]}")


def write_audit_report(path, args, source_users, source_meetings, integrations_report, integrations_issues, meetings_report, meetings_issues):
    payload = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'dry_run': args.dry_run,
        'source_user_count': len(source_users),
        'source_meeting_count': len(source_meetings),
        'integrations_report': dict(integrations_report),
        'integrations_issues': integrations_issues,
        'meetings_report': dict(meetings_report),
        'meetings_issues': meetings_issues,
    }
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\nRelatório JSON salvo em: {report_path}")


def main():
    args = parse_args()
    engine = create_engine(args.source_url)

    with app.app_context():
        with engine.connect() as conn:
            source_users = fetch_source_users(conn)
            source_meetings = fetch_source_meetings(conn, limit=args.limit)

        print(f"Usuários fonte carregados: {len(source_users)}")
        print(f"Reuniões fonte carregadas: {len(source_meetings)}")
        if args.dry_run:
            print('Modo dry-run ativado: nada será gravado no banco do Gestão.')

        integrations_report, integrations_issues = migrate_google_integrations(source_users, dry_run=args.dry_run)
        meetings_report, meetings_issues = migrate_meetings(source_meetings, source_users, dry_run=args.dry_run)

        print_report('Integrações Google', integrations_report)
        print_report('Reuniões', meetings_report)
        print(f"\nPendências de integrações: {len(integrations_issues)}")
        print(f"Pendências de reuniões: {len(meetings_issues)}")

        write_audit_report(
            args.report_json,
            args,
            source_users,
            source_meetings,
            integrations_report,
            integrations_issues,
            meetings_report,
            meetings_issues,
        )


if __name__ == '__main__':
    main()
