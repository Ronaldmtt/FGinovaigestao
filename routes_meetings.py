import json
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models import Client, Meeting, Project, User
from services.meeting_integrations_service import FIREFLIES_PROVIDER, MICROSOFT_PROVIDER, get_user_integration, list_user_integrations
from services.meetings_ai_service import analyze_meeting, generate_meeting_agenda
from services.meetings_calendar_service import (
    GOOGLE_CALENDAR_PROVIDER,
    build_google_calendar_service,
    create_google_calendar_event,
    disconnect_google_credentials_for_user,
    exchange_google_code_for_credentials,
    get_google_authorization_url,
    get_google_calendar_event,
    get_google_credentials_for_user,
    get_shared_google_calendar_integration,
    get_shared_google_credentials,
    list_google_calendar_events,
    save_google_credentials_for_user,
    update_google_calendar_event,
    cancel_google_calendar_event,
)
from services.meetings_fireflies_service import get_transcript, list_transcripts, match_transcript_from_list, _normalize_fireflies_date

HUB_EMAIL = 'hub@inovailab.com'
LOCAL_TIMEZONE = ZoneInfo('America/Sao_Paulo')
TRANSCRIPT_SPEAKER_COLORS = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f1c40f', '#1abc9c', '#f39c12']

meetings_bp = Blueprint('meetings_bp', __name__)


def _validate_api_key():
    expected = os.environ.get('API_SECRET_KEY')
    provided = request.headers.get('X-API-Key')
    if not expected:
        return jsonify({'error': 'API_SECRET_KEY não configurada no servidor'}), 500
    if not provided or provided != expected:
        return jsonify({'error': 'Unauthorized'}), 401
    return None


def _parse_agenda_from_description(description):
    description = (description or '').strip()
    if '--- AGENDA ---' in description:
        return description.split('--- AGENDA ---', 1)[1].strip() or None
    if '--- PAUTA ---' in description:
        return description.split('--- PAUTA ---', 1)[1].strip() or None
    return description or None


def _apply_fireflies_transcript_to_meeting(meeting, transcript):
    if not transcript:
        return False

    meeting.fireflies_transcript_id = transcript.get('id') or meeting.fireflies_transcript_id
    meeting.external_meeting_link = transcript.get('meeting_link') or meeting.external_meeting_link

    sentences = transcript.get('sentences') or []
    if sentences:
        meeting.transcription_content = '\n'.join(
            f"{(item.get('speaker_name') or 'Unknown')}: {(item.get('text') or '').strip()}" if item.get('speaker_name') else (item.get('text') or '').strip()
            for item in sentences if isinstance(item, dict) and (item.get('text') or '').strip()
        )

    summary = transcript.get('summary') or {}
    if summary.get('overview') and not meeting.analysis_summary:
        meeting.analysis_summary = summary.get('overview')

    if meeting.transcription_content and not meeting.results_json:
        results = analyze_meeting(meeting.agenda or '', meeting.transcription_content)
        meeting.analysis_summary = results.get('meeting_summary') or meeting.analysis_summary
        meeting.language = results.get('language')
        meeting.alignment_score = results.get('alignment_score')
        meeting.results_json = json.dumps(results)
        meeting.analysis_status = 'completed'
        meeting.analysis_generated_at = datetime.utcnow()
        meeting.status = 'concluida'

    return True


def _format_mmss(value):
    try:
        total_seconds = max(int(float(value or 0)), 0)
    except Exception:
        total_seconds = 0
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def _parse_fireflies_action_items(summary):
    raw = (summary or {}).get('action_items') if isinstance(summary, dict) else None
    if not raw:
        return []
    groups = []
    current = None
    for line in str(raw).splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith('**') and text.endswith('**'):
            if current:
                groups.append(current)
            current = {'speaker': text.strip('* ').strip(), 'items': []}
            continue
        if current is None:
            current = {'speaker': 'Geral', 'items': []}
        current['items'].append(text)
    if current:
        groups.append(current)
    return [g for g in groups if g.get('items')]


def _parse_fireflies_notes(summary):
    raw = (summary or {}).get('shorthand_bullet') if isinstance(summary, dict) else None
    if not raw:
        return []
    notes = []
    current = None
    for line in str(raw).splitlines():
        text = line.strip()
        if not text:
            continue
        if '**' in text and '(' in text and ')' in text:
            if current:
                notes.append(current)
            time_range = text[text.rfind('(')+1:text.rfind(')')].strip() if '(' in text and ')' in text else ''
            title = re.sub(r'\s*\([^)]*\)\s*$', '', text).replace('**', '').strip()
            current = {
                'title': title,
                'time_range': time_range,
                'lines': []
            }
        else:
            if current is None:
                current = {'title': 'Notas', 'time_range': '', 'lines': []}
            current['lines'].append(text)
    if current:
        notes.append(current)
    return notes


def _build_transcript_blocks(fireflies_transcript):
    sentences = (fireflies_transcript or {}).get('sentences') or []
    if not sentences:
        return []
    speaker_order = []
    for item in sentences:
        speaker = (item.get('speaker_name') or 'Unknown').strip()
        if speaker not in speaker_order:
            speaker_order.append(speaker)
    color_map = {speaker: TRANSCRIPT_SPEAKER_COLORS[idx % len(TRANSCRIPT_SPEAKER_COLORS)] for idx, speaker in enumerate(speaker_order)}
    blocks = []
    for item in sentences:
        speaker = (item.get('speaker_name') or 'Unknown').strip()
        blocks.append({
            'speaker': speaker,
            'time': _format_mmss(item.get('start_time')),
            'text': (item.get('text') or '').strip(),
            'color': color_map.get(speaker, '#6c757d'),
            'initial': (speaker[:1] or '?').upper(),
        })
    return [b for b in blocks if b['text']]


def _parse_iso_datetime(value):
    value = (value or '').strip() if isinstance(value, str) else value
    if not value:
        return None
    try:
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        parsed = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except Exception:
        return None


def _get_meeting_end_time(meeting):
    if not meeting:
        return None
    payload_raw = meeting.raw_provider_payload
    if not payload_raw:
        return None
    try:
        payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    end_data = payload.get('end') or {}
    if isinstance(end_data, dict):
        return _parse_iso_datetime(end_data.get('dateTime')) or _parse_iso_datetime(end_data.get('date'))
    return None


def _update_meeting_status_from_time(meeting):
    if not meeting or meeting.status in {'concluida', 'cancelada'}:
        return False
    end_time = _get_meeting_end_time(meeting)
    reference_time = end_time or meeting.date_time
    if reference_time and reference_time <= datetime.utcnow():
        meeting.status = 'concluida'
        return True
    return False


def _meeting_can_auto_sync_fireflies(meeting):
    if not meeting or meeting.fireflies_transcript_id:
        return False
    if not meeting.title or not meeting.date_time:
        return False
    end_time = _get_meeting_end_time(meeting)
    reference_time = end_time or meeting.date_time
    return reference_time <= datetime.utcnow()


def _extract_agenda_from_google_event(event):
    description_text = (event.get('description') or '').strip()
    if not description_text:
        return None
    if '--- AGENDA ---' in description_text:
        return description_text.split('--- AGENDA ---', 1)[1].strip() or None
    return description_text


def _parse_google_event_datetime(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except Exception:
        return None


def _mark_meeting_sync_success(meeting, event=None):
    if not meeting:
        return
    meeting.last_calendar_sync_at = datetime.utcnow()
    meeting.calendar_sync_error = None
    if isinstance(event, dict):
        updated_raw = event.get('updated')
        parsed_updated = _parse_google_event_datetime(updated_raw)
        if parsed_updated:
            meeting.calendar_last_modified_at = parsed_updated


def _mark_meeting_sync_error(meeting, error):
    if not meeting:
        return
    meeting.last_calendar_sync_at = datetime.utcnow()
    meeting.calendar_sync_error = str(error)[:5000] if error else None


def _sync_meeting_from_google_event(meeting, event):
    if not meeting or not event:
        return False

    changed = False
    new_title = (event.get('summary') or 'Reunião sem título').strip()
    if new_title and meeting.title != new_title:
        meeting.title = new_title
        changed = True

    start_payload = event.get('start') or {}
    start_dt = _parse_google_event_datetime(start_payload.get('dateTime') or start_payload.get('date'), fallback_hour=9)
    if start_dt and meeting.date_time != start_dt:
        meeting.date_time = start_dt
        changed = True

    new_link = event.get('hangoutLink') or event.get('htmlLink')
    if new_link != meeting.external_meeting_link:
        meeting.external_meeting_link = new_link
        changed = True

    owner_email = ((event.get('organizer') or {}).get('email') or meeting.meeting_owner_email or '').strip() or None
    if owner_email != meeting.meeting_owner_email:
        meeting.meeting_owner_email = owner_email
        changed = True

    new_agenda = _extract_agenda_from_google_event(event)
    if new_agenda != meeting.agenda:
        meeting.agenda = new_agenda
        changed = True

    raw_payload = json.dumps(event)
    if raw_payload != meeting.raw_provider_payload:
        meeting.raw_provider_payload = raw_payload
        changed = True

    attendee_emails = []
    for item in (event.get('attendees') or []):
        email = (item.get('email') or '').strip().lower()
        if email and email not in attendee_emails:
            attendee_emails.append(email)
    organizer_email = ((event.get('organizer') or {}).get('email') or '').strip().lower()
    if organizer_email and organizer_email not in attendee_emails:
        attendee_emails.append(organizer_email)
    if HUB_EMAIL not in attendee_emails:
        attendee_emails.append(HUB_EMAIL)
    if meeting.meeting_owner_email and meeting.meeting_owner_email.lower() not in attendee_emails:
        attendee_emails.append(meeting.meeting_owner_email.lower())

    participant_users = User.query.filter(User.email.in_(attendee_emails)).all() if attendee_emails else []
    desired_ids = {user.id for user in participant_users}
    desired_ids.add(meeting.created_by_id)
    current_ids = {user.id for user in meeting.participants}
    if desired_ids != current_ids:
        meeting.participants = list({user.id: user for user in participant_users + ([meeting.creator] if meeting.creator else [])}.values())
        changed = True

    end_payload = event.get('end') or {}
    end_dt = _parse_google_event_datetime(end_payload.get('dateTime') or end_payload.get('date'), fallback_hour=18)
    new_status = 'cancelada' if event.get('status') == 'cancelled' else ('concluida' if end_dt and end_dt <= datetime.utcnow() else 'agendada')
    if meeting.status != new_status:
        meeting.status = new_status
        changed = True

    _mark_meeting_sync_success(meeting, event)
    return changed


def _sync_google_calendar_meeting(meeting):
    if not meeting or meeting.meeting_source != 'google_calendar' or not meeting.google_calendar_event_id:
        return False, None

    try:
        credentials, _source = _get_google_credentials_for_creation(meeting.created_by_id if meeting.created_by_id else None)
        if not credentials:
            _mark_meeting_sync_error(meeting, 'Nenhuma credencial Google disponível para sincronizar a reunião.')
            db.session.commit()
            return False, 'Nenhuma credencial Google disponível para sincronizar a reunião.'
        service = build_google_calendar_service(credentials)
        event = get_google_calendar_event(service, meeting.google_calendar_event_id)
        changed = _sync_meeting_from_google_event(meeting, event)
        db.session.commit()
        return changed, None
    except Exception as e:
        db.session.rollback()
        try:
            _mark_meeting_sync_error(meeting, e)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return False, str(e)


def _get_google_service_for_meeting(meeting):
    credentials, source = _get_google_credentials_for_creation(meeting.created_by_id if meeting and meeting.created_by_id else None)
    if not credentials:
        raise ValueError('Nenhuma credencial Google disponível para esta operação.')
    return build_google_calendar_service(credentials), source


def _build_meeting_description(description, agenda):
    description = (description or '').strip()
    agenda = (agenda or '').strip()
    if agenda:
        return f"{description}\n\n--- AGENDA ---\n{agenda}".strip()
    return description


def _extract_non_internal_attendees(meeting, attendee_emails):
    internal_emails = {u.email.strip().lower() for u in User.query.filter(User.ativo == True).all() if u.email}
    ignored = {HUB_EMAIL.lower()}
    if current_user.is_authenticated and current_user.email:
        ignored.add(current_user.email.lower())
    if meeting and meeting.creator and meeting.creator.email:
        ignored.add(meeting.creator.email.lower())
    return ', '.join(sorted([email for email in attendee_emails if email not in internal_emails and email not in ignored]))


def _auto_sync_fireflies_for_meeting(meeting):
    if not _meeting_can_auto_sync_fireflies(meeting):
        return False, None

    try:
        target_date = meeting.date_time.date().isoformat()
        transcripts, ff_debug = list_transcripts(limit=50, include_debug=True)
        transcripts = transcripts or []
        transcript_match, strategy = match_transcript_from_list(
            transcripts,
            meeting_link=meeting.external_meeting_link,
            title=meeting.title,
            target_date=target_date,
        )

        if not transcript_match:
            details = []
            if meeting.external_meeting_link:
                details.append(f'link={meeting.external_meeting_link}')
            details.append(f'title={meeting.title}')
            details.append(f'date={target_date}')
            candidates = ' | '.join(
                f"{_normalize_fireflies_date(item.get('date'))} :: {repr(item.get('title'))} :: {repr(item.get('meeting_link'))} :: id={item.get('id')}"
                for item in transcripts[:5] if isinstance(item, dict)
            ) or 'nenhum transcript recente retornado'
            debug_bits = f"count={ff_debug.get('count')} token_prefix={ff_debug.get('token_prefix')} payload_keys={ff_debug.get('payload_keys')} data_keys={ff_debug.get('data_keys')} raw_type={ff_debug.get('raw_transcripts_type')} errors={ff_debug.get('error_messages')}"
            return False, f"Transcript não encontrado no Fireflies (single_list_match; {'; '.join(details)}; {debug_bits}; recentes_mesma_lista={candidates})"

        transcript_id = transcript_match.get('id')
        if not transcript_id:
            return False, 'Transcript encontrado no Fireflies sem id válido'

        transcript = get_transcript(transcript_id)
        changed = _apply_fireflies_transcript_to_meeting(meeting, transcript)
        if changed:
            db.session.commit()
        return changed, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def _parse_attendee_emails(raw_value):
    raw = (raw_value or '').strip()
    if not raw:
        return []
    pieces = re.split(r'[;,=\n]+', raw)
    emails = []
    for piece in pieces:
        email = piece.strip()
        if not email:
            continue
        if '@' not in email:
            continue
        emails.append(email)
    deduped = []
    seen = set()
    for email in emails:
        lowered = email.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        deduped.append(email)
    return deduped


def _get_google_credentials_for_creation(user_id=None):
    shared_credentials = get_shared_google_credentials()
    if shared_credentials:
        return shared_credentials, 'shared'

    user_credentials = get_google_credentials_for_user(user_id) if user_id else None
    if user_credentials:
        return user_credentials, 'user'

    return None, None


def _sync_recent_google_calendar_meetings(meetings, limit=12):
    google_meetings = [m for m in (meetings or []) if m.meeting_source == 'google_calendar' and m.google_calendar_event_id]
    if not google_meetings:
        return 0, None

    credentials, _source = _get_google_credentials_for_creation(current_user.id if getattr(current_user, 'is_authenticated', False) else None)
    if not credentials:
        return 0, 'Nenhuma credencial Google disponível para sincronizar reuniões.'

    try:
        service = build_google_calendar_service(credentials)
        changed_count = 0
        for meeting in google_meetings[:limit]:
            try:
                event = get_google_calendar_event(service, meeting.google_calendar_event_id)
                if _sync_meeting_from_google_event(meeting, event):
                    changed_count += 1
            except Exception as e:
                _mark_meeting_sync_error(meeting, e)
                continue
        db.session.commit()
        return changed_count, None
    except Exception as e:
        db.session.rollback()
        return 0, str(e)



def _render_meetings_hub(tab='overview', project_filter=None, user_filter=None, status_filter=None, generated_agenda=None, client_filter=None):
    query = Meeting.query
    if client_filter:
        query = query.join(Project, Meeting.project_id == Project.id).filter(Project.client_id == client_filter)
    if project_filter:
        query = query.filter_by(project_id=project_filter)
    if user_filter:
        query = query.filter(Meeting.participants.any(id=user_filter))
    if status_filter:
        query = query.filter_by(status=status_filter)

    meetings = query.order_by(Meeting.date_time.desc()).all()
    clients = Client.query.order_by(Client.nome.asc()).all()
    projects = Project.query.order_by(Project.nome.asc()).all()
    users = User.query.filter_by(ativo=True).order_by(User.nome.asc(), User.sobrenome.asc()).all()

    total_meetings = Meeting.query.count()
    scheduled_count = Meeting.query.filter_by(status='agendada').count()
    completed_count = Meeting.query.filter_by(status='concluida').count()
    analyzed_count = Meeting.query.filter(Meeting.analysis_summary.isnot(None)).count()
    next_meeting = Meeting.query.filter(Meeting.date_time >= datetime.utcnow()).order_by(Meeting.date_time.asc()).first()
    recent_meetings = Meeting.query.order_by(Meeting.date_time.desc()).limit(5).all()

    google_integration = get_shared_google_calendar_integration() or get_user_integration(current_user.id, GOOGLE_CALENDAR_PROVIDER)
    google_credentials, google_credentials_source = _get_google_credentials_for_creation(current_user.id)
    google_connected = bool(google_credentials) or bool(google_integration and google_integration.is_enabled)
    all_integrations = list_user_integrations(current_user.id)
    google_events = []
    google_events_error = None
    google_sync_count = 0
    meetings_sync_error = None

    if tab in {'overview', 'list'}:
        google_sync_count, meetings_sync_error = _sync_recent_google_calendar_meetings(meetings, limit=12 if tab == 'list' else 6)

    if google_connected and tab in {'overview', 'calendar', 'integrations', 'agendas'}:
        try:
            if google_credentials:
                service = build_google_calendar_service(google_credentials)
                google_events = list_google_calendar_events(service, max_results=10, include_recent=True)
        except Exception as e:
            google_events_error = str(e)

    return render_template(
        'meetings.html',
        tab=tab,
        meetings=meetings,
        clients=clients,
        projects=projects,
        users=users,
        selected_client=client_filter,
        selected_project=project_filter,
        selected_user=user_filter,
        selected_status=status_filter,
        total_meetings=total_meetings,
        scheduled_count=scheduled_count,
        completed_count=completed_count,
        analyzed_count=analyzed_count,
        next_meeting=next_meeting,
        recent_meetings=recent_meetings,
        google_connected=google_connected,
        google_integration=google_integration,
        all_integrations=all_integrations,
        google_events=google_events,
        google_events_error=google_events_error,
        generated_agenda=generated_agenda,
        fireflies_provider=FIREFLIES_PROVIDER,
        microsoft_provider=MICROSOFT_PROVIDER,
        google_credentials_source=google_credentials_source,
        google_sync_count=google_sync_count,
        meetings_sync_error=meetings_sync_error,
    )


@meetings_bp.route('/meetings', methods=['GET'])
@login_required
def meetings_hub():
    tab = request.args.get('tab', 'overview')
    client_filter = request.args.get('client_id')
    project_filter = request.args.get('project_id')
    user_filter = request.args.get('user_id')
    status_filter = request.args.get('status')
    return _render_meetings_hub(tab=tab, project_filter=project_filter, user_filter=user_filter, status_filter=status_filter, client_filter=client_filter)


@meetings_bp.route('/meetings/<int:meeting_id>', methods=['GET'])
@login_required
def meeting_detail(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)

    calendar_synced = False
    calendar_sync_error = None
    if meeting.meeting_source == 'google_calendar' and meeting.google_calendar_event_id:
        calendar_synced, calendar_sync_error = _sync_google_calendar_meeting(meeting)

    status_updated = _update_meeting_status_from_time(meeting)

    fireflies_auto_synced = False
    fireflies_error = calendar_sync_error
    if _meeting_can_auto_sync_fireflies(meeting):
        fireflies_auto_synced, auto_sync_error = _auto_sync_fireflies_for_meeting(meeting)
        if auto_sync_error:
            fireflies_error = auto_sync_error

    if status_updated and not fireflies_auto_synced and not calendar_synced:
        db.session.commit()

    results = {}
    if meeting.results_json:
        try:
            results = json.loads(meeting.results_json)
        except Exception:
            results = {}

    fireflies_transcript = None
    if meeting.fireflies_transcript_id:
        try:
            fireflies_transcript = get_transcript(meeting.fireflies_transcript_id)
        except Exception as e:
            fireflies_error = str(e)

    media_audio_url = (fireflies_transcript.get('audio_url') if fireflies_transcript else None) or meeting.audio_url
    media_video_url = (fireflies_transcript.get('video_url') if fireflies_transcript else None) or meeting.video_url
    fireflies_summary = (fireflies_transcript or {}).get('summary') or {}
    fireflies_action_groups = _parse_fireflies_action_items(fireflies_summary)
    fireflies_notes = _parse_fireflies_notes(fireflies_summary)
    transcript_blocks = _build_transcript_blocks(fireflies_transcript)

    edit_payload = {}
    if meeting.raw_provider_payload:
        try:
            edit_payload = json.loads(meeting.raw_provider_payload)
        except Exception:
            edit_payload = {}
    edit_attendee_emails = []
    for item in (edit_payload.get('attendees') or []):
        email = (item.get('email') or '').strip()
        if email:
            edit_attendee_emails.append(email)
    edit_description = (edit_payload.get('description') or '').strip() if isinstance(edit_payload, dict) else ''
    if '--- AGENDA ---' in edit_description:
        edit_description = edit_description.split('--- AGENDA ---', 1)[0].strip()

    return render_template(
        'meeting_detail.html',
        meeting=meeting,
        results=results,
        fireflies_transcript=fireflies_transcript,
        fireflies_error=fireflies_error,
        fireflies_auto_synced=fireflies_auto_synced,
        calendar_synced=calendar_synced,
        calendar_sync_error=calendar_sync_error,
        fireflies_pending=bool(_meeting_can_auto_sync_fireflies(meeting) and not meeting.fireflies_transcript_id),
        meeting_end_time=_get_meeting_end_time(meeting),
        media_audio_url=media_audio_url,
        media_video_url=media_video_url,
        fireflies_action_groups=fireflies_action_groups,
        fireflies_notes=fireflies_notes,
        transcript_blocks=transcript_blocks,
        edit_attendee_emails=edit_attendee_emails,
        edit_description=edit_description,
        now_utc=datetime.utcnow(),
    )


@meetings_bp.route('/api/meetings/create', methods=['POST'])
@login_required
def create_meeting():
    title = (request.form.get('title') or '').strip()
    meeting_date = (request.form.get('meeting_date') or '').strip()
    start_time = (request.form.get('start_time') or '').strip()
    end_time = (request.form.get('end_time') or '').strip()
    agenda = (request.form.get('agenda') or '').strip()
    project_id = request.form.get('project_id')
    participant_ids = request.form.getlist('participants')

    if not title or not meeting_date or not start_time:
        flash('Título, data e hora de início são obrigatórios.', 'error')
        return redirect(url_for('meetings_bp.meetings_hub', tab='list'))

    try:
        dt = datetime.strptime(f'{meeting_date} {start_time}', '%Y-%m-%d %H:%M')
    except ValueError:
        flash('Formato de data/hora inválido.', 'error')
        return redirect(url_for('meetings_bp.meetings_hub', tab='list'))

    raw_provider_payload = None
    if end_time:
        try:
            end_dt = datetime.strptime(f'{meeting_date} {end_time}', '%Y-%m-%d %H:%M')
            raw_provider_payload = json.dumps({'end': {'dateTime': end_dt.isoformat()}})
        except ValueError:
            flash('Hora de término inválida.', 'error')
            return redirect(url_for('meetings_bp.meetings_hub', tab='list'))

    new_meeting = Meeting(
        title=title,
        date_time=dt,
        project_id=project_id if project_id else None,
        created_by_id=current_user.id,
        meeting_source='internal',
        analysis_status='pending',
        agenda=agenda or None,
        raw_provider_payload=raw_provider_payload,
    )

    if participant_ids:
        for p_id in participant_ids:
            user = User.query.get(p_id)
            if user:
                new_meeting.participants.append(user)

    if current_user not in new_meeting.participants:
        new_meeting.participants.append(current_user)

    db.session.add(new_meeting)
    db.session.commit()

    flash('Reunião agendada com sucesso!', 'success')
    return redirect(url_for('meetings_bp.meetings_hub', tab='list'))


@meetings_bp.route('/meetings/analyze', methods=['POST'])
@login_required
def analyze_manual_meeting():
    title = (request.form.get('title') or '').strip()
    agenda = (request.form.get('agenda') or '').strip()
    transcription = (request.form.get('transcription') or '').strip()
    meeting_date = (request.form.get('meeting_date') or '').strip()
    project_id = request.form.get('project_id')

    if not title or not agenda or not transcription:
        flash('Título, pauta e transcrição são obrigatórios para análise.', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='new-analysis'))

    date_time = datetime.utcnow()
    if meeting_date:
        try:
            parsed_date = datetime.strptime(meeting_date, '%Y-%m-%d')
            date_time = parsed_date.replace(hour=12, minute=0)
        except ValueError:
            pass

    results = analyze_meeting(agenda, transcription)
    meeting = Meeting(
        title=title,
        date_time=date_time,
        project_id=project_id if project_id else None,
        agenda=agenda,
        transcription_content=transcription,
        analysis_summary=results.get('meeting_summary'),
        language=results.get('language'),
        alignment_score=results.get('alignment_score'),
        results_json=json.dumps(results),
        created_by_id=current_user.id,
        meeting_source='manual_analysis',
        analysis_status='completed',
        analysis_generated_at=datetime.utcnow(),
        status='concluida',
    )
    meeting.participants.append(current_user)
    db.session.add(meeting)
    db.session.commit()

    flash('Análise de reunião gerada com sucesso.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/meetings/agenda/generate', methods=['POST'])
@login_required
def generate_agenda_for_meeting():
    topic = (request.form.get('topic') or '').strip()
    description = (request.form.get('description') or '').strip()
    language = (request.form.get('language') or 'pt').strip()
    project_id = (request.form.get('project_id') or '').strip()

    if not topic or not description:
        flash('Informe tópico e descrição para gerar a pauta.', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='agendas'))

    generated = generate_meeting_agenda(topic, description, language)
    generated['description'] = description
    generated['project_id'] = project_id or ''
    flash('Pauta gerada com sucesso. Revise o texto abaixo e use na criação da reunião.', 'success')
    return _render_meetings_hub(tab='agendas', generated_agenda=generated)


@meetings_bp.route('/meetings/integrations/google/connect')
@login_required
def connect_google_calendar():
    authorization_url, _state = get_google_authorization_url()
    return redirect(authorization_url)


@meetings_bp.route('/meetings/integrations/google/callback')
@meetings_bp.route('/oauth2callback')
@login_required
def google_calendar_callback():
    code = request.args.get('code')
    if not code:
        flash('Código de autorização do Google não recebido.', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='integrations'))

    credentials = exchange_google_code_for_credentials(code)
    save_google_credentials_for_user(current_user.id, credentials, account_email=current_user.email)
    flash('Google Calendar conectado com sucesso.', 'success')
    return redirect(url_for('meetings_bp.meetings_hub', tab='integrations'))


@meetings_bp.route('/meetings/integrations/google/disconnect')
@login_required
def disconnect_google_calendar():
    disconnect_google_credentials_for_user(current_user.id)
    flash('Integração com Google Calendar desconectada.', 'success')
    return redirect(url_for('meetings_bp.meetings_hub', tab='integrations'))


@meetings_bp.route('/meetings/calendar/create', methods=['POST'])
@login_required
def create_calendar_meeting():
    title = (request.form.get('title') or '').strip()
    description = (request.form.get('description') or '').strip()
    agenda = (request.form.get('agenda') or '').strip()
    project_id = request.form.get('project_id')
    start_date = request.form.get('start_date')
    start_time = request.form.get('start_time')
    end_date = request.form.get('end_date') or start_date
    end_time = request.form.get('end_time')
    attendees_raw = request.form.get('attendees', '')

    if not all([title, start_date, start_time, end_date, end_time]):
        flash('Preencha título, data e horários para criar o evento no calendário.', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='agendas'))

    credentials, credentials_source = _get_google_credentials_for_creation(current_user.id)
    if not credentials:
        flash('Nenhuma credencial do Google Calendar está configurada para criar a reunião.', 'warning')
        return redirect(url_for('meetings_bp.meetings_hub', tab='integrations'))

    start_dt = datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M')
    end_dt = datetime.strptime(f'{end_date} {end_time}', '%Y-%m-%d %H:%M')
    attendees = _parse_attendee_emails(attendees_raw)
    if current_user.email and current_user.email not in attendees:
        attendees.append(current_user.email)
    if HUB_EMAIL not in attendees:
        attendees.append(HUB_EMAIL)

    participant_users = User.query.filter(User.email.in_(attendees)).all() if attendees else []

    service = build_google_calendar_service(credentials)
    full_description = description.strip()
    if agenda:
        full_description = f"{full_description}\n\n--- AGENDA ---\n{agenda}".strip()

    try:
        event = create_google_calendar_event(service, title, full_description, start_dt, end_dt, attendees=attendees)
    except Exception as e:
        flash(f'Falha ao criar evento no Google Calendar: {e}', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='agendas'))

    meeting = Meeting(
        title=title,
        date_time=start_dt,
        project_id=project_id if project_id else None,
        created_by_id=current_user.id,
        meeting_source='google_calendar',
        google_calendar_event_id=event.get('id'),
        external_meeting_link=event.get('hangoutLink') or event.get('htmlLink'),
        raw_provider_payload=json.dumps(event),
        status='agendada',
        meeting_owner_email=current_user.email,
        agenda=agenda or None,
        last_calendar_sync_at=datetime.utcnow(),
        calendar_last_modified_at=_parse_google_event_datetime(event.get('updated')),
        calendar_sync_error=None,
    )
    meeting.participants.append(current_user)
    for user in participant_users:
        if user not in meeting.participants:
            meeting.participants.append(user)
    db.session.add(meeting)
    db.session.commit()

    origem = 'a conta compartilhada do hub' if credentials_source == 'shared' else 'uma conta Google de fallback'
    flash(f'Evento criado no Google Calendar com sucesso usando {origem}. O hub e o criador foram adicionados automaticamente como convidados.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/meetings/<int:meeting_id>/edit', methods=['POST'])
@login_required
def update_calendar_meeting_route(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    if meeting.meeting_source != 'google_calendar' or not meeting.google_calendar_event_id:
        flash('A edição inline está disponível apenas para reuniões sincronizadas com Google Calendar.', 'warning')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    title = (request.form.get('title') or '').strip()
    description = (request.form.get('description') or '').strip()
    agenda = (request.form.get('agenda') or '').strip()
    start_date = (request.form.get('start_date') or '').strip()
    start_time = (request.form.get('start_time') or '').strip()
    end_date = (request.form.get('end_date') or start_date or '').strip()
    end_time = (request.form.get('end_time') or '').strip()
    attendees_raw = request.form.get('attendees', '')

    if not all([title, start_date, start_time, end_date, end_time]):
        flash('Título, datas e horários são obrigatórios para editar a reunião.', 'danger')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    try:
        start_dt = datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M')
        end_dt = datetime.strptime(f'{end_date} {end_time}', '%Y-%m-%d %H:%M')
    except ValueError:
        flash('Formato de data/hora inválido para edição da reunião.', 'danger')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    attendees = _parse_attendee_emails(attendees_raw)
    creator_email = (meeting.creator.email if meeting.creator and meeting.creator.email else current_user.email or '').strip().lower()
    if creator_email and creator_email not in attendees:
        attendees.append(creator_email)
    if HUB_EMAIL not in attendees:
        attendees.append(HUB_EMAIL)

    try:
        service, _source = _get_google_service_for_meeting(meeting)
        existing_event = get_google_calendar_event(service, meeting.google_calendar_event_id)
        updated_event = update_google_calendar_event(
            service,
            meeting.google_calendar_event_id,
            title=title,
            description=_build_meeting_description(description, agenda),
            start_time=start_dt,
            end_time=end_dt,
            attendees=attendees,
            existing_event=existing_event,
        )
        _sync_meeting_from_google_event(meeting, updated_event)
        db.session.commit()
        flash('Reunião atualizada no Google Calendar e sincronizada no sistema.', 'success')
    except Exception as e:
        db.session.rollback()
        try:
            _mark_meeting_sync_error(meeting, e)
            db.session.commit()
        except Exception:
            db.session.rollback()
        flash(f'Falha ao editar reunião no Google Calendar: {e}', 'danger')

    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/meetings/<int:meeting_id>/cancel', methods=['POST'])
@login_required
def cancel_calendar_meeting_route(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)

    if meeting.meeting_source == 'google_calendar' and meeting.google_calendar_event_id:
        try:
            service, _source = _get_google_service_for_meeting(meeting)
            cancel_google_calendar_event(service, meeting.google_calendar_event_id)
        except Exception as e:
            db.session.rollback()
            try:
                _mark_meeting_sync_error(meeting, e)
                db.session.commit()
            except Exception:
                db.session.rollback()
            flash(f'Falha ao cancelar reunião no Google Calendar: {e}', 'danger')
            return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    meeting.status = 'cancelada'
    _mark_meeting_sync_success(meeting, {'updated': datetime.utcnow().isoformat()})
    db.session.commit()
    flash('Reunião cancelada no sistema e no Google Calendar.', 'success')
    return redirect(url_for('meetings_bp.meetings_hub', tab='list'))


@meetings_bp.route('/meetings/sync-google', methods=['POST'])
@login_required
def sync_google_meetings_route():
    meetings = Meeting.query.filter(
        Meeting.meeting_source == 'google_calendar',
        Meeting.google_calendar_event_id.isnot(None)
    ).order_by(Meeting.date_time.desc()).limit(25).all()

    synced, error = _sync_recent_google_calendar_meetings(meetings, limit=25)
    if error:
        flash(f'Falha ao sincronizar reuniões com Google Calendar: {error}', 'warning')
    else:
        flash(f'Sincronização concluída. {synced} reunião(ões) atualizada(s) a partir do Google Calendar.', 'success')

    return redirect(url_for('meetings_bp.meetings_hub', tab=request.args.get('tab', 'overview')))


@meetings_bp.route('/meetings/<int:meeting_id>/calendar-analysis', methods=['POST'])
@login_required
def analyze_calendar_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    transcription = (request.form.get('transcription') or '').strip()

    if not transcription:
        flash('A transcrição é obrigatória para analisar a reunião.', 'danger')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    results = analyze_meeting(meeting.agenda or '', transcription)
    meeting.transcription_content = transcription
    meeting.analysis_summary = results.get('meeting_summary')
    meeting.language = results.get('language')
    meeting.alignment_score = results.get('alignment_score')
    meeting.results_json = json.dumps(results)
    meeting.analysis_status = 'completed'
    meeting.analysis_generated_at = datetime.utcnow()
    meeting.status = 'concluida'
    db.session.commit()

    flash('Análise da reunião gerada com sucesso.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/meetings/<int:meeting_id>/sync-fireflies', methods=['POST'])
@login_required
def sync_fireflies_for_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    status_updated = _update_meeting_status_from_time(meeting)

    synced, error = _auto_sync_fireflies_for_meeting(meeting)
    if error:
        if status_updated:
            db.session.commit()
        flash(f'Erro ao sincronizar com o Fireflies: {error}', 'warning')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))
    if not synced:
        if status_updated:
            db.session.commit()
        flash('Nenhum transcript correspondente foi encontrado no Fireflies para esta reunião ainda.', 'warning')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    flash('Reunião sincronizada com o Fireflies com sucesso.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/meetings/calendar/import/<event_id>')
@login_required
def import_calendar_event(event_id):
    credentials = get_shared_google_credentials()
    if not credentials:
        flash('Nenhuma credencial compartilhada do hub está configurada para o módulo de reuniões.', 'warning')
        return redirect(url_for('meetings_bp.meetings_hub', tab='integrations'))

    service = build_google_calendar_service(credentials)
    event = get_google_calendar_event(service, event_id)
    start_str = event.get('start', {}).get('dateTime')
    start_dt = datetime.utcnow()
    if start_str:
        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00')).replace(tzinfo=None)

    existing = Meeting.query.filter_by(google_calendar_event_id=event_id).first()
    if existing:
        flash('Esse evento já foi importado para o módulo de reuniões.', 'info')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=existing.id))

    attendees = event.get('attendees') or []
    attendee_emails = [item.get('email') for item in attendees if item.get('email')]
    if HUB_EMAIL not in attendee_emails:
        attendee_emails.append(HUB_EMAIL)
    participant_users = User.query.filter(User.email.in_(attendee_emails)).all() if attendee_emails else []

    description_text = (event.get('description') or '').strip()
    agenda_text = None
    if '--- AGENDA ---' in description_text:
        parts = description_text.split('--- AGENDA ---', 1)
        description_text = parts[0].strip()
        agenda_text = parts[1].strip() or None
    elif description_text:
        agenda_text = description_text

    meeting = Meeting(
        title=event.get('summary') or 'Reunião sem título',
        date_time=start_dt,
        created_by_id=current_user.id,
        meeting_source='google_calendar',
        google_calendar_event_id=event_id,
        external_meeting_link=event.get('hangoutLink') or event.get('htmlLink'),
        raw_provider_payload=json.dumps(event),
        status='agendada',
        meeting_owner_email=(event.get('organizer') or {}).get('email') or current_user.email,
        agenda=agenda_text,
        last_calendar_sync_at=datetime.utcnow(),
        calendar_last_modified_at=_parse_google_event_datetime(event.get('updated')),
        calendar_sync_error=None,
    )
    meeting.participants.append(current_user)
    for user in participant_users:
        if user not in meeting.participants:
            meeting.participants.append(user)
    db.session.add(meeting)
    db.session.commit()

    flash('Evento importado para o módulo de reuniões.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/api/meetings/sync-google', methods=['POST'])
def api_sync_google_meetings():
    auth_error = _validate_api_key()
    if auth_error:
        return auth_error

    limit = request.args.get('limit', default=50, type=int) or 50
    meetings = Meeting.query.filter(
        Meeting.meeting_source == 'google_calendar',
        Meeting.google_calendar_event_id.isnot(None)
    ).order_by(Meeting.date_time.desc()).limit(max(1, min(limit, 100))).all()

    synced, error = _sync_recent_google_calendar_meetings(meetings, limit=max(1, min(limit, 100)))
    if error:
        return jsonify({'success': False, 'error': error, 'synced': synced}), 500
    return jsonify({'success': True, 'synced': synced, 'checked': len(meetings)})


@meetings_bp.route('/api/create_meeting', methods=['POST'])
def api_create_meeting():
    auth_error = _validate_api_key()
    if auth_error:
        return auth_error

    try:
        data = request.get_json() or {}
        user_email = (data.get('user_email') or '').strip().lower()
        title = (data.get('title') or '').strip()
        start_str = data.get('start_time')
        end_str = data.get('end_time')
        description = (data.get('description') or '').strip()
        attendees = data.get('attendees') or []

        if not all([user_email, title, start_str, end_str]):
            return jsonify({'error': 'Missing required fields: user_email, title, start_time, end_time'}), 400

        user = User.query.filter(db.func.lower(User.email) == user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        credentials = get_shared_google_credentials()
        if not credentials:
            return jsonify({'error': 'No shared hub Google Calendar integration available'}), 400

        start_time = datetime.fromisoformat(start_str.replace('Z', '+00:00')).replace(tzinfo=None)
        end_time = datetime.fromisoformat(end_str.replace('Z', '+00:00')).replace(tzinfo=None)

        if not isinstance(attendees, list):
            return jsonify({'error': 'attendees must be a list'}), 400
        attendees = [str(email).strip() for email in attendees if str(email).strip()]
        if HUB_EMAIL not in attendees:
            attendees.append(HUB_EMAIL)

        service = build_google_calendar_service(credentials)
        event = create_google_calendar_event(service, title, description, start_time, end_time, attendees=attendees)

        agenda = _parse_agenda_from_description(description) or 'Pauta enviada via API'
        participant_users = User.query.filter(User.email.in_(attendees)).all() if attendees else []

        meeting = Meeting(
            title=title,
            date_time=start_time,
            agenda=agenda,
            transcription_content='Para analisar esta reunião, insira a transcrição',
            created_by_id=user.id,
            meeting_source='api_google_calendar',
            google_calendar_event_id=event.get('id'),
            external_meeting_link=event.get('hangoutLink') or event.get('htmlLink'),
            raw_provider_payload=json.dumps(event),
            meeting_owner_email=user.email,
            status='agendada',
            analysis_status='pending',
        )
        if user not in meeting.participants:
            meeting.participants.append(user)
        for participant in participant_users:
            if participant not in meeting.participants:
                meeting.participants.append(participant)

        db.session.add(meeting)
        db.session.commit()

        return jsonify({
            'success': True,
            'meeting_id': meeting.id,
            'google_event_id': event.get('id'),
            'google_link': event.get('htmlLink') or event.get('hangoutLink'),
            'hub_invited': HUB_EMAIL in attendees,
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@meetings_bp.route('/api/get_transcript', methods=['POST'])
def api_get_transcript():
    auth_error = _validate_api_key()
    if auth_error:
        return auth_error

    try:
        data = request.get_json() or {}
        title = (data.get('title') or '').strip()
        target_date = (data.get('date') or '').strip()
        if not title or not target_date:
            return jsonify({'error': 'Missing required fields: title, date'}), 400

        transcript_match = find_transcript_by_title_and_date(title, target_date, limit=100)
        if not transcript_match:
            return jsonify({
                'found': False,
                'message': 'No meeting found with matching title and date',
                'search_criteria': {'title': title, 'date': target_date}
            }), 404

        transcript = get_transcript(transcript_match.get('id')) or {}
        sentences = transcript.get('sentences') or []
        formatted = []
        for item in sentences:
            speaker = (item.get('speaker_name') or '').strip()
            text = (item.get('text') or '').strip()
            if not text:
                continue
            formatted.append(f'{speaker}: {text}' if speaker else text)

        summary = transcript.get('summary') or {}
        return jsonify({
            'found': True,
            'fireflies_id': transcript.get('id'),
            'title': transcript.get('title'),
            'date': target_date,
            'audio_url': transcript.get('audio_url'),
            'video_url': transcript.get('video_url'),
            'meeting_link': transcript.get('meeting_link'),
            'summary': summary.get('overview', ''),
            'transcription': '\n'.join(formatted),
            'raw_transcript': transcript,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
