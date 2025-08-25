from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import app, db
from models import User, Client, Project, Task
from forms import LoginForm, UserForm, ClientForm, ProjectForm, TaskForm, TranscriptionTaskForm
from openai_service import process_project_transcription, generate_tasks_from_transcription

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash and form.password.data and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Email ou senha inválidos.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Estatísticas básicas
    stats = {}
    if current_user.is_admin:
        stats = {
            'total_users': User.query.count(),
            'total_clients': Client.query.count(),
            'total_projects': Project.query.count(),
            'total_tasks': Task.query.count()
        }
    else:
        stats = {
            'my_projects': Project.query.filter_by(responsible_id=current_user.id).count(),
            'my_tasks': Task.query.filter_by(assigned_user_id=current_user.id).count(),
            'clients_created': Client.query.filter_by(creator_id=current_user.id).count(),
            'pending_tasks': Task.query.filter_by(assigned_user_id=current_user.id, status='pendente').count()
        }
    
    return render_template('dashboard.html', stats=stats)

# Rotas de Administração
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem acessar esta área.', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
def admin_new_user():
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            nome=form.nome.data,
            sobrenome=form.sobrenome.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data) if form.password.data else "",
            is_admin=form.is_admin.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/users.html', form=form)

# Rotas de Clientes
@app.route('/clients')
@login_required
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/clients/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            endereco=form.endereco.data,
            creator_id=current_user.id
        )
        db.session.add(client)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('clients'))
    
    return render_template('clients.html', form=form)

# Rotas de Projetos
@app.route('/projects')
@login_required
def projects():
    if current_user.is_admin:
        projects = Project.query.all()
    else:
        # Usuários veem apenas projetos que criaram ou são responsáveis ou fazem parte da equipe
        projects = Project.query.filter(
            (Project.responsible_id == current_user.id) |
            (Project.team_members.contains(current_user))
        ).distinct().all()
    
    return render_template('projects.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            nome=form.nome.data,
            client_id=form.client_id.data,
            responsible_id=form.responsible_id.data,
            transcricao=form.transcricao.data
        )
        
        # Processar transcrição com IA se fornecida
        if form.transcricao.data:
            ai_result = process_project_transcription(form.transcricao.data)
            if ai_result:
                project.contexto_justificativa = ai_result.get('contexto_justificativa')
                project.descricao_resumida = ai_result.get('descricao_resumida')
                project.problema_oportunidade = ai_result.get('problema_oportunidade')
                project.objetivos = ai_result.get('objetivos')
                project.alinhamento_estrategico = ai_result.get('alinhamento_estrategico')
                project.escopo_projeto = ai_result.get('escopo_projeto')
                project.fora_escopo = ai_result.get('fora_escopo')
                project.premissas = ai_result.get('premissas')
                project.restricoes = ai_result.get('restricoes')
        
        db.session.add(project)
        db.session.flush()  # Para obter o ID do projeto
        
        # Adicionar membros da equipe
        if form.team_members.data:
            team_member = User.query.get(form.team_members.data)
            if team_member:
                project.team_members.append(team_member)
        
        # Gerar tarefas automáticas se houver transcrição
        if form.transcricao.data:
            auto_tasks = generate_tasks_from_transcription(form.transcricao.data, project.nome)
            for task_data in auto_tasks:
                task = Task(
                    titulo=task_data['titulo'],
                    descricao=task_data['descricao'],
                    project_id=project.id,
                    status='pendente'
                )
                db.session.add(task)
        
        db.session.commit()
        flash('Projeto criado com sucesso!', 'success')
        return redirect(url_for('projects'))
    
    return render_template('projects.html', form=form)

@app.route('/projects/<int:id>')
@login_required
def project_detail(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem acesso ao projeto
    if not current_user.is_admin and current_user.id != project.responsible_id and current_user not in project.team_members:
        flash('Você não tem acesso a este projeto.', 'danger')
        return redirect(url_for('projects'))
    
    return render_template('project_detail.html', project=project)

# Rotas de Tarefas
@app.route('/tasks')
@login_required
def tasks():
    if current_user.is_admin:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(assigned_user_id=current_user.id).all()
    
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            project_id=form.project_id.data,
            assigned_user_id=form.assigned_user_id.data if form.assigned_user_id.data else None,
            data_conclusao=form.data_conclusao.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tasks'))
    
    return render_template('tasks.html', form=form)

@app.route('/tasks/transcription', methods=['GET', 'POST'])
@login_required
def transcription_task():
    form = TranscriptionTaskForm()
    if form.validate_on_submit():
        project = Project.query.get(form.project_id.data)
        if project:
            # Gerar tarefas com IA
            auto_tasks = generate_tasks_from_transcription(form.transcricao.data, project.nome)
            
            for task_data in auto_tasks:
                task = Task(
                    titulo=task_data['titulo'],
                    descricao=task_data['descricao'],
                    project_id=project.id,
                    status='pendente'
                )
                db.session.add(task)
            
            db.session.commit()
            flash(f'{len(auto_tasks)} tarefas foram geradas automaticamente!', 'success')
            return redirect(url_for('kanban'))
    
    return render_template('tasks.html', transcription_form=form)

# Kanban
@app.route('/kanban')
@login_required
def kanban():
    # Filtros
    project_filter = request.args.get('project_id', type=int)
    client_filter = request.args.get('client_id', type=int)
    my_tasks = request.args.get('my_tasks', type=bool)
    
    query = Task.query
    
    if not current_user.is_admin and my_tasks:
        query = query.filter_by(assigned_user_id=current_user.id)
    elif not current_user.is_admin and not my_tasks:
        # Mostrar tarefas dos projetos que o usuário participa
        user_projects = Project.query.filter(
            (Project.responsible_id == current_user.id) |
            (Project.team_members.contains(current_user))
        ).distinct().all()
        project_ids = [p.id for p in user_projects]
        query = query.filter(Task.project_id.in_(project_ids))
    
    if project_filter:
        query = query.filter_by(project_id=project_filter)
    
    if client_filter:
        query = query.join(Project).filter(Project.client_id == client_filter)
    
    tasks = query.all()
    
    # Organizar tarefas por status
    task_columns = {
        'pendente': [],
        'em_andamento': [],
        'concluida': []
    }
    
    for task in tasks:
        task_columns[task.status].append(task)
    
    # Para os filtros
    projects = Project.query.all()
    clients = Client.query.all()
    
    return render_template('kanban.html', 
                         task_columns=task_columns, 
                         projects=projects, 
                         clients=clients,
                         current_filters={
                             'project_id': project_filter,
                             'client_id': client_filter,
                             'my_tasks': my_tasks
                         })

@app.route('/api/tasks/<int:task_id>/status', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Verificar permissão
    if not current_user.is_admin and task.assigned_user_id != current_user.id:
        project = task.project
        if current_user.id != project.responsible_id and current_user not in project.team_members:
            return jsonify({'error': 'Sem permissão'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status in ['pendente', 'em_andamento', 'concluida']:
        task.status = new_status
        
        if new_status == 'concluida':
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None
            
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Status inválido'}), 400

@app.route('/api/projects/<int:client_id>')
@login_required
def get_projects_by_client(client_id):
    projects = Project.query.filter_by(client_id=client_id).all()
    project_list = [{'id': p.id, 'nome': p.nome} for p in projects]
    return jsonify(project_list)
