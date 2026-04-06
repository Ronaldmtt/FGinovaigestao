import json
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models import Meeting, Project, User
from services.meeting_integrations_service import get_user_integration
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
    list_google_calendar_events,
    save_google_credentials_for_user,
)
from services.meetings_fireflies_service import find_transcript_by_title_and_date, get_transcript

meetings_bp = Blueprint('meetings_bp', __name__)


@meetings_bp.route('/meetings', methods=['GET'])
@login_required
def meetings_hub():
    tab = request.args.get('tab', 'overview')
    project_filter = request.args.get('project_id')
    user_filter = request.args.get('user_id')
    status_filter = request.args.get('status')

    query = Meeting.query
    if project_filter:
        query = query.filter_by(project_id=project_filter)
    if user_filter:
        query = query.filter(Meeting.participants.any(id=user_filter))
    if status_filter:
        query = query.filter_by(status=status_filter)

    meetings = query.order_by(Meeting.date_time.desc()).all()
    projects = Project.query.order_by(Project.nome.asc()).all()
    users = User.query.filter_by(ativo=True).order_by(User.nome.asc(), User.sobrenome.asc()).all()

    total_meetings = Meeting.query.count()
    scheduled_count = Meeting.query.filter_by(status='agendada').count()
    completed_count = Meeting.query.filter_by(status='concluida').count()
    analyzed_count = Meeting.query.filter(Meeting.analysis_summary.isnot(None)).count()
    next_meeting = Meeting.query.filter(Meeting.date_time >= datetime.utcnow()).order_by(Meeting.date_time.asc()).first()
    recent_meetings = Meeting.query.order_by(Meeting.date_time.desc()).limit(5).all()

    google_integration = get_user_integration(current_user.id, GOOGLE_CALENDAR_PROVIDER)
    google_connected = bool(google_integration and google_integration.is_enabled)
    google_events = []
    google_events_error = None

    if google_connected and tab in {'overview', 'calendar', 'integrations'}:
        try:
            credentials = get_google_credentials_for_user(current_user.id)
            if credentials:
                service = build_google_calendar_service(credentials)
                google_events = list_google_calendar_events(service, max_results=10, include_recent=True)
        except Exception as e:
            google_events_error = str(e)

    return render_template(
        'meetings.html',
        tab=tab,
        meetings=meetings,
        projects=projects,
        users=users,
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
        google_events=google_events,
        google_events_error=google_events_error,
    )


@meetings_bp.route('/meetings/<int:meeting_id>', methods=['GET'])
@login_required
def meeting_detail(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)

    results = {}
    if meeting.results_json:
        try:
            results = json.loads(meeting.results_json)
        except Exception:
            results = {}

    fireflies_transcript = None
    fireflies_error = None
    if meeting.fireflies_transcript_id:
        try:
            fireflies_transcript = get_transcript(meeting.fireflies_transcript_id)
        except Exception as e:
            fireflies_error = str(e)

    return render_template(
        'meeting_detail.html',
        meeting=meeting,
        results=results,
        fireflies_transcript=fireflies_transcript,
        fireflies_error=fireflies_error,
    )


@meetings_bp.route('/api/meetings/create', methods=['POST'])
@login_required
def create_meeting():
    title = request.form.get('title')
    date_time_str = request.form.get('date_time')
    project_id = request.form.get('project_id')
    participant_ids = request.form.getlist('participants')

    if not title or not date_time_str:
        flash('Título e Data/Hora são obrigatórios', 'error')
        return redirect(url_for('meetings_bp.meetings_hub', tab='list'))

    try:
        dt = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Formato de data inválido.', 'error')
        return redirect(url_for('meetings_bp.meetings_hub', tab='list'))

    new_meeting = Meeting(
        title=title,
        date_time=dt,
        project_id=project_id if project_id else None,
        created_by_id=current_user.id,
        meeting_source='internal',
        analysis_status='pending',
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

    if not topic or not description:
        flash('Informe tópico e descrição para gerar a pauta.', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='agendas'))

    generated = generate_meeting_agenda(topic, description, language)
    flash('Pauta gerada com sucesso. Revise o texto abaixo e use na criação da reunião.', 'success')
    return render_template(
        'meetings.html',
        tab='agendas',
        meetings=Meeting.query.order_by(Meeting.date_time.desc()).all(),
        projects=Project.query.order_by(Project.nome.asc()).all(),
        users=User.query.filter_by(ativo=True).order_by(User.nome.asc(), User.sobrenome.asc()).all(),
        selected_project=None,
        selected_user=None,
        selected_status=None,
        total_meetings=Meeting.query.count(),
        scheduled_count=Meeting.query.filter_by(status='agendada').count(),
        completed_count=Meeting.query.filter_by(status='concluida').count(),
        analyzed_count=Meeting.query.filter(Meeting.analysis_summary.isnot(None)).count(),
        next_meeting=Meeting.query.filter(Meeting.date_time >= datetime.utcnow()).order_by(Meeting.date_time.asc()).first(),
        recent_meetings=Meeting.query.order_by(Meeting.date_time.desc()).limit(5).all(),
        google_connected=bool(get_user_integration(current_user.id, GOOGLE_CALENDAR_PROVIDER)),
        google_events=[],
        google_events_error=None,
        generated_agenda=generated,
    )


@meetings_bp.route('/meetings/integrations/google/connect')
@login_required
def connect_google_calendar():
    authorization_url, _state = get_google_authorization_url()
    return redirect(authorization_url)


@meetings_bp.route('/meetings/integrations/google/callback')
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
    start_date = request.form.get('start_date')
    start_time = request.form.get('start_time')
    end_date = request.form.get('end_date') or start_date
    end_time = request.form.get('end_time')
    attendees_raw = request.form.get('attendees', '')

    if not all([title, start_date, start_time, end_date, end_time]):
        flash('Preencha título, data e horários para criar o evento no calendário.', 'danger')
        return redirect(url_for('meetings_bp.meetings_hub', tab='calendar'))

    credentials = get_google_credentials_for_user(current_user.id)
    if not credentials:
        flash('Conecte o Google Calendar antes de criar eventos.', 'warning')
        return redirect(url_for('meetings_bp.meetings_hub', tab='integrations'))

    start_dt = datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M')
    end_dt = datetime.strptime(f'{end_date} {end_time}', '%Y-%m-%d %H:%M')
    attendees = [email.strip() for email in attendees_raw.split(',') if email.strip()]

    service = build_google_calendar_service(credentials)
    event = create_google_calendar_event(service, title, description, start_dt, end_dt, attendees=attendees)

    meeting = Meeting(
        title=title,
        date_time=start_dt,
        created_by_id=current_user.id,
        meeting_source='google_calendar',
        google_calendar_event_id=event.get('id'),
        external_meeting_link=event.get('hangoutLink') or event.get('htmlLink'),
        raw_provider_payload=json.dumps(event),
        status='agendada',
        meeting_owner_email=current_user.email,
    )
    meeting.participants.append(current_user)
    db.session.add(meeting)
    db.session.commit()

    flash('Evento criado no Google Calendar com sucesso.', 'success')
    return redirect(url_for('meetings_bp.meetings_hub', tab='calendar'))


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

    target_date = meeting.date_time.date().isoformat() if meeting.date_time else ''
    transcript_match = find_transcript_by_title_and_date(meeting.title, target_date, limit=100)
    if not transcript_match:
        flash('Nenhum transcript correspondente foi encontrado no Fireflies pelo título/data.', 'warning')
        return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))

    transcript_id = transcript_match.get('id')
    transcript = get_transcript(transcript_id)
    meeting.fireflies_transcript_id = transcript_id
    meeting.audio_url = transcript.get('audio_url') or meeting.audio_url
    meeting.video_url = transcript.get('video_url') or meeting.video_url
    meeting.external_meeting_link = transcript.get('meeting_link') or meeting.external_meeting_link

    sentences = transcript.get('sentences') or []
    if sentences:
        meeting.transcription_content = '\n'.join((item.get('text') or '').strip() for item in sentences if (item.get('text') or '').strip())

    summary = transcript.get('summary') or {}
    if summary.get('overview') and not meeting.analysis_summary:
        meeting.analysis_summary = summary.get('overview')

    db.session.commit()
    flash('Reunião sincronizada com o Fireflies com sucesso.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))


@meetings_bp.route('/meetings/calendar/import/<event_id>')
@login_required
def import_calendar_event(event_id):
    credentials = get_google_credentials_for_user(current_user.id)
    if not credentials:
        flash('Conecte o Google Calendar antes de importar eventos.', 'warning')
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
        agenda=(event.get('description') or '').strip() or None,
    )
    meeting.participants.append(current_user)
    db.session.add(meeting)
    db.session.commit()

    flash('Evento importado para o módulo de reuniões.', 'success')
    return redirect(url_for('meetings_bp.meeting_detail', meeting_id=meeting.id))
