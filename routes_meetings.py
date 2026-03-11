from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
from models import Meeting, Project, User

meetings_bp = Blueprint('meetings_bp', __name__)

@meetings_bp.route('/meetings', methods=['GET'])
@login_required
def meetings_hub():
    """Página principal do Hub de Reuniões com filtros e listagem."""
    project_filter = request.args.get('project_id')
    user_filter = request.args.get('user_id')
    
    query = Meeting.query
    
    if project_filter:
        query = query.filter_by(project_id=project_filter)
        
    if user_filter:
        query = query.filter(Meeting.participants.any(id=user_filter))
        
    meetings = query.order_by(Meeting.date_time.desc()).all()
    
    projects = Project.query.all()
    users = User.query.filter_by(ativo=True).all()
    
    return render_template('meetings.html', 
                         meetings=meetings, 
                         projects=projects, 
                         users=users,
                         selected_project=project_filter,
                         selected_user=user_filter)

@meetings_bp.route('/meetings/<int:meeting_id>', methods=['GET'])
@login_required
def meeting_detail(meeting_id):
    """Página de detalhes da reunião (transcrição, análise, participantes)."""
    meeting = Meeting.query.get_or_404(meeting_id)
    return render_template('meeting_detail.html', meeting=meeting)

@meetings_bp.route('/api/meetings/create', methods=['POST'])
@login_required
def create_meeting():
    """API para criar uma nova reunião e convidar/anexar usuários."""
    title = request.form.get('title')
    date_time_str = request.form.get('date_time')
    project_id = request.form.get('project_id')
    participant_ids = request.form.getlist('participants') # Multiselect
    
    if not title or not date_time_str:
        flash('Título e Data/Hora são obrigatórios', 'error')
        return redirect(url_for('meetings_bp.meetings_hub'))
        
    try:
        dt = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Formato de data inválido.', 'error')
        return redirect(url_for('meetings_bp.meetings_hub'))
        
    new_meeting = Meeting(
        title=title,
        date_time=dt,
        project_id=project_id if project_id else None,
        created_by_id=current_user.id
    )
    
    # Adicionar participantes reais via relação Muitos-para-Muitos
    if participant_ids:
        for p_id in participant_ids:
            user = User.query.get(p_id)
            if user:
                new_meeting.participants.append(user)
                
    # O criador também entra por padrão na visualizaçao de participantes
    if current_user not in new_meeting.participants:
        new_meeting.participants.append(current_user)
        
    db.session.add(new_meeting)
    db.session.commit()
    
    flash('Reunião agendada com sucesso!', 'success')
    return redirect(url_for('meetings_bp.meetings_hub'))
