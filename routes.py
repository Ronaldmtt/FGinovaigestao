from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
import httpx
import secrets
import string
import json
import os
from app import app, db
from models import User, Client, Project, Task, TodoItem
from forms import LoginForm, UserForm, EditUserForm, ClientForm, ProjectForm, TaskForm, TranscriptionTaskForm, ManualProjectForm, ManualTaskForm, ForgotPasswordForm, ResetPasswordForm, ChangePasswordForm, ImportDataForm
from openai_service import process_project_transcription, generate_tasks_from_transcription
from email_service import enviar_email_nova_tarefa, enviar_email_mudanca_status, enviar_email_alteracao_data, enviar_email_tarefa_editada, enviar_email_resumo_tarefas

def requires_permission(permission_field):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.is_admin:
                return f(*args, **kwargs)
            if not getattr(current_user, permission_field, False):
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
    
    users = User.query.order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()
    form = UserForm()
    return render_template('admin/users.html', users=users, form=form)

@app.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
def admin_new_user():
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = UserForm()
    if form.validate_on_submit():
        # Debug: Log dos valores recebidos
        app.logger.debug(f"=== DEBUG CRIAÇÃO DE USUÁRIO ===")
        app.logger.debug(f"is_admin checkbox: {form.is_admin.data}")
        app.logger.debug(f"acesso_clientes: {form.acesso_clientes.data}")
        app.logger.debug(f"acesso_projetos: {form.acesso_projetos.data}")
        app.logger.debug(f"acesso_tarefas: {form.acesso_tarefas.data}")
        app.logger.debug(f"acesso_kanban: {form.acesso_kanban.data}")
        app.logger.debug(f"acesso_crm: {form.acesso_crm.data}")
        
        user = User(
            nome=form.nome.data,
            sobrenome=form.sobrenome.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data) if form.password.data else "",
            is_admin=form.is_admin.data,
            acesso_clientes=form.acesso_clientes.data,
            acesso_projetos=form.acesso_projetos.data,
            acesso_tarefas=form.acesso_tarefas.data,
            acesso_kanban=form.acesso_kanban.data,
            acesso_crm=form.acesso_crm.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Debug: Confirmar o que foi salvo
        app.logger.debug(f"Usuário salvo - is_admin: {user.is_admin}, acesso_tarefas: {user.acesso_tarefas}, acesso_kanban: {user.acesso_kanban}")
        
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/users.html', form=form)

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    form = EditUserForm(original_email=user.email, obj=user)
    
    if form.validate_on_submit():
        user.nome = form.nome.data
        user.sobrenome = form.sobrenome.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        user.acesso_clientes = form.acesso_clientes.data
        user.acesso_projetos = form.acesso_projetos.data
        user.acesso_tarefas = form.acesso_tarefas.data
        user.acesso_kanban = form.acesso_kanban.data
        user.acesso_crm = form.acesso_crm.data
        user.receber_notificacoes = form.receber_notificacoes.data
        
        # Só atualiza a senha se uma nova foi fornecida
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Não permitir que o admin delete a si mesmo
    if user.id == current_user.id:
        flash('Você não pode deletar sua própria conta.', 'danger')
        return redirect(url_for('admin_users'))
    
    # Verificar se o usuário tem projetos ou tarefas associadas
    if user.projects_responsible.count() > 0 or user.assigned_tasks.count() > 0:
        flash('Não é possível deletar este usuário pois ele tem projetos ou tarefas associadas.', 'danger')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Usuário removido com sucesso!', 'success')
    return redirect(url_for('admin_users'))

# Rotas de Clientes
@app.route('/clients')
@login_required
@requires_permission('acesso_clientes')
def clients():
    # Filtros
    search_term = request.args.get('search', '')
    creator_filter = request.args.get('creator_id', type=int)
    
    # Query base
    query = Client.query
    
    # Aplicar filtros
    if search_term:
        query = query.filter(
            (Client.nome.ilike(f'%{search_term}%')) |
            (Client.email.ilike(f'%{search_term}%'))
        )
    
    if creator_filter:
        query = query.filter_by(created_by=creator_filter)
    
    clients = query.order_by(Client.nome).all()
    
    form = ClientForm()
    all_users = User.query.filter_by(is_admin=False).all()
    
    return render_template('clients.html', 
                         clients=clients, 
                         form=form,
                         all_users=all_users,
                         current_search=search_term,
                         current_creator_id=creator_filter)

@app.route('/clients/new', methods=['GET', 'POST'])
@login_required
@requires_permission('acesso_clientes')
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

@app.route('/clients/<int:id>/generate-public-link', methods=['POST'])
@login_required
@requires_permission('acesso_clientes')
def generate_public_link(id):
    client = Client.query.get_or_404(id)
    
    # Verificar se usuário tem acesso
    if not current_user.is_admin and client.creator_id != current_user.id:
        flash('Você não tem permissão para gerar link para este cliente.', 'danger')
        return redirect(url_for('clients'))
    
    # Gerar código único
    if not client.public_code:
        # Gerar código de 8 caracteres alfanuméricos
        alphabet = string.ascii_uppercase + string.digits
        client.public_code = ''.join(secrets.choice(alphabet) for _ in range(8))
        db.session.commit()
    
    # Retornar dados do link
    return jsonify({
        'success': True,
        'public_code': client.public_code,
        'public_url': url_for('public_access', _external=True)
    })

@app.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
@login_required
@requires_permission('acesso_clientes')
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    
    form = ClientForm(obj=client)
    
    if form.validate_on_submit():
        client.nome = form.nome.data
        client.email = form.email.data
        client.telefone = form.telefone.data
        client.endereco = form.endereco.data
        
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clients'))
    
    return render_template('edit_client.html', form=form, client=client)

@app.route('/clients/delete/<int:client_id>', methods=['POST'])
@login_required
@requires_permission('acesso_clientes')
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    
    # Verificar se o cliente tem projetos associados
    if client.projects:
        flash('Não é possível excluir este cliente pois ele tem projetos associados.', 'danger')
        return redirect(url_for('clients'))
    
    db.session.delete(client)
    db.session.commit()
    flash('Cliente removido com sucesso!', 'success')
    return redirect(url_for('clients'))

# Rotas de Projetos
@app.route('/projects')
@login_required
@requires_permission('acesso_projetos')
def projects():
    # Filtros
    client_filter = request.args.get('client_id', type=int)
    responsible_filter = request.args.get('responsible_id', type=int)
    status_filter = request.args.get('status')
    
    # Query base
    if current_user.is_admin:
        query = Project.query
    else:
        # Usuários veem apenas projetos que criaram ou são responsáveis ou fazem parte da equipe
        query = Project.query.filter(
            (Project.responsible_id == current_user.id) |
            (Project.team_members.contains(current_user))
        ).distinct()
    
    # Aplicar filtros
    if client_filter:
        query = query.filter_by(client_id=client_filter)
    
    if responsible_filter:
        query = query.filter_by(responsible_id=responsible_filter)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    projects = query.order_by(Project.nome).all()
    
    form = ProjectForm()
    all_clients = Client.query.order_by(Client.nome).all()
    all_users = User.query.filter_by(is_admin=False).all()
    
    return render_template('projects.html', 
                         projects=projects, 
                         form=form, 
                         all_clients=all_clients,
                         all_users=all_users,
                         current_filters={
                             'client_id': client_filter,
                             'responsible_id': responsible_filter,
                             'status': status_filter
                         })

@app.route('/projects/new', methods=['GET', 'POST'])
@login_required
@requires_permission('acesso_projetos')
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        # Criar projeto primeiro
        project = Project(
            nome=form.nome.data,
            client_id=form.client_id.data,
            responsible_id=form.responsible_id.data,
            status=form.status.data,
            transcricao=form.transcricao.data
        )
        
        db.session.add(project)
        db.session.flush()  # Para obter o ID do projeto
        
        # Adicionar membros da equipe
        if form.team_members.data:
            team_member = User.query.get(form.team_members.data)
            if team_member:
                project.team_members.append(team_member)
        
        # Commit inicial para salvar o projeto
        db.session.commit()
        
        # Tentar processar com IA em segundo plano (sem bloquear)
        success_message = 'Projeto criado com sucesso!'
        
        # Processar com IA automaticamente na criação (em duas etapas separadas)
        if form.transcricao.data and len(form.transcricao.data.strip()) > 10:
            try:
                # Etapa 1: Processar dados do projeto com transcrição completa
                print("Etapa 1: Processando dados do projeto...")
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
                    
                    # Salvar dados do projeto primeiro
                    db.session.commit()
                    print("Dados do projeto processados com sucesso!")
                    
                    # Etapa 2: Gerar tarefas com transcrição completa
                    print("Etapa 2: Gerando tarefas...")
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
                    print("Tarefas geradas com sucesso!")
                    success_message = 'Projeto criado e processado com IA em duas etapas com sucesso!'
                else:
                    success_message = 'Projeto criado, mas houve problema no processamento dos dados pela IA.'
                    
            except Exception as e:
                print(f"Erro no processamento da IA: {e}")
                success_message = 'Projeto criado com sucesso! A IA não conseguiu processar a transcrição no momento.'
        else:
            success_message = 'Projeto criado com sucesso!'
        
        flash(success_message, 'success')
        return redirect(url_for('projects'))
    
    clients = Client.query.all()
    users = User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()
    return render_template('projects.html', form=form, clients=clients, users=users)

@app.route('/projects/new-manual', methods=['POST'])
@login_required
def new_manual_project():
    nome = request.form.get('nome')
    client_id = request.form.get('client_id')
    responsible_id = request.form.get('responsible_id')
    status = request.form.get('status')
    team_member_ids = request.form.getlist('team_member_ids')  # Múltiplos membros
    
    # Criar o projeto
    project = Project(
        nome=nome,
        client_id=client_id,
        responsible_id=responsible_id,
        status=status,
        contexto_justificativa=request.form.get('descricao_resumida'),
        descricao_resumida=request.form.get('descricao_resumida'),
        problema_oportunidade=request.form.get('problema_oportunidade'),
        objetivos=request.form.get('objetivos'),
        alinhamento_estrategico=request.form.get('alinhamento_estrategico'),
        escopo_projeto=request.form.get('escopo_projeto'),
        fora_escopo=request.form.get('fora_escopo'),
        premissas=request.form.get('premissas'),
        restricoes=request.form.get('restricoes')
    )
    
    db.session.add(project)
    db.session.flush()  # Para obter o ID do projeto
    
    # Adicionar múltiplos membros da equipe
    if team_member_ids:
        for member_id in team_member_ids:
            user = User.query.get(int(member_id))
            if user:
                project.team_members.append(user)
    
    db.session.commit()
    flash('Projeto criado manualmente com sucesso!', 'success')
    return redirect(url_for('projects'))

@app.route('/projects/<int:id>')
@login_required
def project_detail(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem acesso ao projeto
    if not current_user.is_admin and current_user.id != project.responsible_id and current_user not in project.team_members:
        flash('Você não tem acesso a este projeto.', 'danger')
        return redirect(url_for('projects'))
    
    clients = Client.query.all()
    users = User.query.all()
    return render_template('project_detail.html', project=project, clients=clients, users=users)

@app.route('/projects/<int:id>/edit', methods=['POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem permissão para editar
    if not current_user.is_admin and current_user.id != project.responsible_id:
        flash('Você não tem permissão para editar este projeto.', 'danger')
        return redirect(url_for('project_detail', id=id))
    
    # Atualizar dados do projeto
    project.nome = request.form.get('nome')
    project.client_id = request.form.get('client_id')
    project.responsible_id = request.form.get('responsible_id')
    project.status = request.form.get('status')
    
    # Atualizar membros da equipe (limpar e adicionar novos)
    team_member_ids = request.form.getlist('team_member_ids')  # Múltiplos membros
    project.team_members.clear()  # Limpar membros atuais
    if team_member_ids:
        for member_id in team_member_ids:
            user = User.query.get(int(member_id))
            if user:
                project.team_members.append(user)
    
    try:
        db.session.commit()
        flash('Projeto atualizado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao atualizar o projeto. Tente novamente.', 'danger')
        print(f"Erro ao editar projeto: {e}")
    
    return redirect(url_for('project_detail', id=id))

@app.route('/projects/<int:id>/process-ai', methods=['POST'])
@login_required
def process_project_ai(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem acesso ao projeto
    if not current_user.is_admin and current_user.id != project.responsible_id and current_user not in project.team_members:
        flash('Você não tem acesso a este projeto.', 'danger')
        return redirect(url_for('projects'))
    
    if not project.transcricao:
        flash('Este projeto não possui transcrição para processar.', 'warning')
        return redirect(url_for('project_detail', id=id))
    
    try:
        # Processar transcrição com IA
        ai_result = process_project_transcription(project.transcricao)
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
            
            # Gerar tarefas automáticas se ainda não existem
            if not project.tasks:
                auto_tasks = generate_tasks_from_transcription(project.transcricao, project.nome)
                for task_data in auto_tasks:
                    task = Task(
                        titulo=task_data['titulo'],
                        descricao=task_data['descricao'],
                        project_id=project.id,
                        status='pendente'
                    )
                    db.session.add(task)
            
            db.session.commit()
            flash('Projeto processado com IA com sucesso!', 'success')
        else:
            flash('Houve problema no processamento da IA. Tente novamente mais tarde.', 'warning')
            
    except Exception as e:
        print(f"Erro no processamento da IA: {e}")
        flash('Erro ao processar com IA. Tente novamente mais tarde.', 'warning')
    
    return redirect(url_for('project_detail', id=id))

@app.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem permissão para deletar (admin ou responsável)
    if not current_user.is_admin and current_user.id != project.responsible_id:
        flash('Você não tem permissão para deletar este projeto.', 'danger')
        return redirect(url_for('project_detail', id=id))
    
    try:
        # Deletar todas as tarefas relacionadas ao projeto
        Task.query.filter_by(project_id=id).delete()
        
        # Deletar o projeto
        project_name = project.nome
        db.session.delete(project)
        db.session.commit()
        
        flash(f'Projeto "{project_name}" foi deletado com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar o projeto. Tente novamente.', 'danger')
        print(f"Erro ao deletar projeto: {e}")
        return redirect(url_for('project_detail', id=id))
    
    return redirect(url_for('projects'))

# Rotas de Tarefas
@app.route('/tasks')
@login_required
@requires_permission('acesso_tarefas')
def tasks():
    # Filtros
    project_filter = request.args.get('project_id', type=int)
    client_filter = request.args.get('client_id', type=int)
    user_filter = request.args.get('user_id', type=int)
    status_filter = request.args.get('status')
    
    # Query base
    query = Task.query
    
    # Filtro de permissões
    if not current_user.is_admin:
        query = query.filter_by(assigned_user_id=current_user.id)
    
    # Aplicar filtros
    if project_filter:
        query = query.filter_by(project_id=project_filter)
    
    if client_filter:
        query = query.join(Project).filter(Project.client_id == client_filter)
    
    if user_filter:
        query = query.filter(Task.assigned_user_id == user_filter)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    tasks = query.all()
    
    form = TaskForm()
    transcription_form = TranscriptionTaskForm()
    all_projects = Project.query.join(Client).order_by(Client.nome, Project.nome).all()
    all_clients = Client.query.order_by(Client.nome).all()
    all_users = User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()
    
    return render_template('tasks.html', 
                         tasks=tasks, 
                         form=form, 
                         transcription_form=transcription_form, 
                         all_projects=all_projects,
                         all_clients=all_clients,
                         all_users=all_users,
                         current_filters={
                             'project_id': project_filter,
                             'client_id': client_filter,
                             'user_id': user_filter,
                             'status': status_filter
                         })

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

@app.route('/tasks/<int:task_id>/edit', methods=['GET'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Verificar permissão
    if not current_user.is_admin and task.assigned_user_id != current_user.id:
        project = task.project
        if current_user.id != project.responsible_id and current_user not in project.team_members:
            flash('Sem permissão para editar esta tarefa.', 'danger')
            return redirect(url_for('tasks'))
    
    return redirect(url_for('kanban') + f'#task-{task_id}')

@app.route('/tasks/new-manual', methods=['POST'])
@login_required 
def new_manual_task():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    project_id = request.form.get('project_id')
    assigned_user_id = request.form.get('assigned_user_id')
    data_conclusao = request.form.get('data_conclusao')
    status = request.form.get('status')
    
    # Converter data se fornecida
    data_conclusao_obj = None
    if data_conclusao:
        from datetime import datetime
        data_conclusao_obj = datetime.strptime(data_conclusao, '%Y-%m-%d').date()
    
    # Criar tarefa
    task = Task(
        titulo=titulo,
        descricao=descricao,
        project_id=project_id,
        assigned_user_id=assigned_user_id if assigned_user_id else None,
        data_conclusao=data_conclusao_obj,
        status=status
    )
    
    db.session.add(task)
    db.session.commit()
    
    # Enviar notificação por email se houver usuário atribuído
    if task.assigned_user_id:
        usuario = User.query.get(task.assigned_user_id)
        projeto = Project.query.get(task.project_id)
        if usuario and projeto:
            try:
                enviar_email_nova_tarefa(usuario, task, projeto)
            except Exception as e:
                app.logger.error(f"Erro ao enviar email de nova tarefa: {e}")
    
    flash('Tarefa criada manualmente com sucesso!', 'success')
    return redirect(url_for('tasks'))

# Rotas públicas para clientes
@app.route('/public')
def public_access():
    return render_template('public_access.html')

@app.route('/public/verify', methods=['POST'])
def verify_public_code():
    code = request.form.get('code', '').strip().upper()
    
    if not code:
        flash('Por favor, insira o código de acesso.', 'danger')
        return redirect(url_for('public_access'))
    
    client = Client.query.filter_by(public_code=code).first()
    
    if not client:
        flash('Código de acesso inválido.', 'danger')
        return redirect(url_for('public_access'))
    
    # Redirecionar para timeline do cliente
    return redirect(url_for('client_timeline', code=code))

@app.route('/public/timeline/<code>')
def client_timeline(code):
    client = Client.query.filter_by(public_code=code).first_or_404()
    
    # Buscar todos os projetos do cliente
    projects = Project.query.filter_by(client_id=client.id).order_by(Project.created_at.desc()).all()
    
    # Buscar todas as tarefas dos projetos do cliente
    all_tasks = []
    for project in projects:
        for task in project.tasks:
            all_tasks.append({
                'task': task,
                'project': project
            })
    
    # Ordenar tarefas por data de criação
    all_tasks.sort(key=lambda x: x['task'].created_at, reverse=True)
    
    return render_template('client_timeline.html', 
                         client=client, 
                         projects=projects, 
                         all_tasks=all_tasks)

@app.route('/public/project-details/<int:project_id>/<code>')
def public_project_details(project_id, code):
    # Verificar se o código é válido
    client = Client.query.filter_by(public_code=code).first_or_404()
    
    # Verificar se o projeto pertence ao cliente
    project = Project.query.filter_by(id=project_id, client_id=client.id).first_or_404()
    
    # Preparar dados completos do projeto
    project_data = {
        'id': project.id,
        'nome': project.nome,
        'status': project.status,
        'created_at': project.created_at.isoformat(),
        'data_inicio': project.created_at.strftime('%d/%m/%Y') if project.created_at else None,
        'data_fim': None,  # Campo não existe no modelo atual
        'responsible_name': project.responsible.full_name if project.responsible else 'Não definido',
        'team_members': [member.full_name for member in project.team_members],
        'descricao_resumida': project.descricao_resumida,
        'problema_oportunidade': project.problema_oportunidade,
        'objetivos': project.objetivos,
        'alinhamento_estrategico': project.alinhamento_estrategico,
        'escopo_projeto': project.escopo_projeto,
        'fora_escopo': project.fora_escopo,
        'premissas': project.premissas,
        'restricoes': project.restricoes
    }
    
    return jsonify({
        'success': True,
        'project': project_data
    })

@app.route('/public/project-tasks/<int:project_id>/<code>')
def public_project_tasks(project_id, code):
    # Verificar se o código é válido
    client = Client.query.filter_by(public_code=code).first_or_404()
    
    # Verificar se o projeto pertence ao cliente
    project = Project.query.filter_by(id=project_id, client_id=client.id).first_or_404()
    
    # Buscar apenas as tarefas deste projeto
    tasks = Task.query.filter_by(project_id=project.id).order_by(Task.created_at.desc()).all()
    
    # Preparar dados das tarefas
    tasks_data = []
    for task in tasks:
        task_info = {
            'id': task.id,
            'titulo': task.titulo,
            'descricao': task.descricao,
            'status': task.status,
            'created_at': task.created_at.strftime('%d/%m/%Y às %H:%M'),
            'data_conclusao': task.data_conclusao.strftime('%d/%m/%Y') if task.data_conclusao else None,
            'assigned_user': task.assigned_user.full_name if task.assigned_user else None,
            'todos': [{'text': todo.texto, 'completed': todo.completed} for todo in task.todos]
        }
        tasks_data.append(task_info)
    
    return jsonify({
        'success': True,
        'project_name': project.nome,
        'tasks': tasks_data
    })


@app.route('/public/project-stats/<int:project_id>/<code>')
def public_project_stats(project_id, code):
    try:
        # Verificar se o código é válido
        client = Client.query.filter_by(public_code=code).first_or_404()
        
        # Verificar se o projeto pertence ao cliente
        project = Project.query.filter_by(id=project_id, client_id=client.id).first_or_404()
        
        # Calcular estatísticas
        tasks = Task.query.filter_by(project_id=project.id).all()
        total_tasks = len(tasks)
        
        pending_tasks = len([t for t in tasks if t.status == 'pendente'])
        in_progress_tasks = len([t for t in tasks if t.status == 'em_andamento'])
        completed_tasks = len([t for t in tasks if t.status == 'concluida'])
        
        progress_percent = round((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        
        stats_data = {
            'total_tasks': total_tasks,
            'pending': pending_tasks,
            'in_progress': in_progress_tasks,
            'completed': completed_tasks,
            'progress_percent': progress_percent,
            'start_date': project.data_inicio.strftime('%d/%m/%Y') if project.data_inicio else None,
            'end_date': project.data_fim.strftime('%d/%m/%Y') if project.data_fim else None
        }
        
        return jsonify({
            'success': True,
            'stats': stats_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/projects/<int:id>/data')
@login_required
def get_project_data(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem acesso ao projeto
    if not current_user.is_admin and current_user.id != project.responsible_id:
        return jsonify({'success': False, 'message': 'Acesso negado'}), 403
    
    # Buscar dados necessários para o formulário
    clients = Client.query.all()
    users = User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()
    
    # Preparar dados do projeto
    project_data = {
        'id': project.id,
        'nome': project.nome,
        'client_id': project.client_id,
        'responsible_id': project.responsible_id,
        'status': project.status,
        'team_members': [member.id for member in project.team_members],
        'descricao_resumida': project.descricao_resumida,
        'problema_oportunidade': project.problema_oportunidade,
        'objetivos': project.objetivos,
        'alinhamento_estrategico': project.alinhamento_estrategico,
        'escopo_projeto': project.escopo_projeto,
        'fora_escopo': project.fora_escopo,
        'premissas': project.premissas,
        'restricoes': project.restricoes
    }
    
    clients_data = [{'id': c.id, 'nome': c.nome} for c in clients]
    users_data = [{'id': u.id, 'full_name': u.full_name} for u in users]
    
    return jsonify({
        'success': True,
        'project': project_data,
        'clients': clients_data,
        'users': users_data
    })

@app.route('/projects/<int:id>/edit', methods=['POST'])
@login_required
def update_project(id):
    project = Project.query.get_or_404(id)
    
    # Verificar se o usuário tem acesso ao projeto
    if not current_user.is_admin and current_user.id != project.responsible_id:
        flash('Você não tem permissão para editar este projeto.', 'danger')
        return redirect(url_for('projects'))
    
    # Atualizar dados do projeto
    project.nome = request.form.get('nome')
    project.client_id = request.form.get('client_id')
    project.responsible_id = request.form.get('responsible_id')
    project.status = request.form.get('status')
    project.descricao_resumida = request.form.get('descricao_resumida')
    project.problema_oportunidade = request.form.get('problema_oportunidade')
    project.objetivos = request.form.get('objetivos')
    project.alinhamento_estrategico = request.form.get('alinhamento_estrategico')
    project.escopo_projeto = request.form.get('escopo_projeto')
    project.fora_escopo = request.form.get('fora_escopo')
    project.premissas = request.form.get('premissas')
    project.restricoes = request.form.get('restricoes')
    
    # Limpar membros atuais da equipe e adicionar novo se selecionado
    project.team_members.clear()
    team_member_id = request.form.get('team_member_id')
    if team_member_id:
        user = User.query.get(team_member_id)
        if user:
            project.team_members.append(user)
    
    db.session.commit()
    flash('Projeto atualizado com sucesso!', 'success')
    return redirect(url_for('projects'))

@app.route('/tasks/new-kanban', methods=['POST'])
@login_required
def new_task_kanban():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    project_id = request.form.get('project_id')
    assigned_user_id = request.form.get('assigned_user_id')
    data_conclusao = request.form.get('data_conclusao')
    status = request.form.get('status')
    
    # Converter data se fornecida
    data_conclusao_obj = None
    if data_conclusao:
        from datetime import datetime
        data_conclusao_obj = datetime.strptime(data_conclusao, '%Y-%m-%d').date()
    
    # Criar tarefa
    task = Task(
        titulo=titulo,
        descricao=descricao,
        project_id=project_id,
        assigned_user_id=assigned_user_id if assigned_user_id else None,
        data_conclusao=data_conclusao_obj,
        status=status
    )
    
    db.session.add(task)
    db.session.commit()
    
    flash('Tarefa criada com sucesso!', 'success')
    return redirect(url_for('kanban'))

@app.route('/tasks/transcription', methods=['GET', 'POST'])
@login_required
def transcription_task():
    form = TranscriptionTaskForm()
    if form.validate_on_submit():
        project = Project.query.get(form.project_id.data)
        if project:
            try:
                # Gerar tarefas com IA
                auto_tasks = generate_tasks_from_transcription(form.transcricao.data, project.nome)
                
                tasks_created = 0
                for task_data in auto_tasks:
                    task = Task(
                        titulo=task_data['titulo'],
                        descricao=task_data['descricao'],
                        project_id=project.id,
                        status='pendente'
                    )
                    db.session.add(task)
                    tasks_created += 1
                
                db.session.commit()
                flash(f'{tasks_created} tarefas foram geradas automaticamente!', 'success')
                
            except Exception as e:
                print(f"Erro ao gerar tarefas: {e}")
                flash('Erro ao processar a transcrição. Tente novamente mais tarde.', 'warning')
            
            return redirect(url_for('kanban'))
    
    return render_template('tasks.html', transcription_form=form)

# Kanban
@app.route('/kanban')
@login_required
@requires_permission('acesso_kanban')
def kanban():
    # Filtros
    project_filter = request.args.get('project_id', type=int)
    client_filter = request.args.get('client_id', type=int)
    user_filter = request.args.get('user_id', type=int)
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
    
    if user_filter:
        query = query.filter(Task.assigned_user_id == user_filter)
    
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
    projects = Project.query.join(Client).order_by(Client.nome, Project.nome).all()
    clients = Client.query.all()
    
    # Todos os usuários para o modal de edição e filtros
    all_users = User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()
    
    return render_template('kanban.html', 
                         task_columns=task_columns, 
                         projects=projects, 
                         clients=clients,
                         all_users=all_users,
                         current_filters={
                             'project_id': project_filter,
                             'client_id': client_filter,
                             'user_id': user_filter,
                             'my_tasks': my_tasks
                         })

# API Routes para tarefas
@app.route('/api/tasks/<int:task_id>')
@login_required
def api_get_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    todos = [{'id': todo.id, 'texto': todo.texto, 'completed': todo.completed} for todo in task.todos]
    
    return jsonify({
        'id': task.id,
        'titulo': task.titulo,
        'descricao': task.descricao,
        'assigned_user_id': task.assigned_user_id,
        'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
        'status': task.status,
        'todos': todos
    })

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    # Guardar valores antigos para comparação
    status_antigo = task.status
    data_antigo = task.data_conclusao
    titulo_antigo = task.titulo
    descricao_antiga = task.descricao
    
    try:
        # Atualizar campos
        titulo_mudou = False
        descricao_mudou = False
        status_mudou = False
        data_mudou = False
        
        if 'titulo' in data:
            if task.titulo != data['titulo']:
                titulo_mudou = True
            task.titulo = data['titulo']
        if 'descricao' in data:
            if task.descricao != data['descricao']:
                descricao_mudou = True
            task.descricao = data['descricao']
        if 'assigned_user_id' in data:
            task.assigned_user_id = data['assigned_user_id'] if data['assigned_user_id'] else None
        if 'status' in data:
            if task.status != data['status']:
                status_mudou = True
            task.status = data['status']
            # Atualizar data de conclusão baseado no status
            if data['status'] == 'concluida':
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        if 'data_conclusao' in data:
            nova_data = None
            if data['data_conclusao']:
                nova_data = datetime.strptime(data['data_conclusao'], '%Y-%m-%d').date()
            
            if task.data_conclusao != nova_data:
                data_mudou = True
            task.data_conclusao = nova_data
        
        # Atualizar to-do's
        if 'todos' in data:
            # Primeiro, remover todos os to-do's existentes
            TodoItem.query.filter_by(task_id=task.id).delete()
            
            # Adicionar os novos to-do's
            for todo_data in data['todos']:
                if todo_data.get('texto', '').strip():  # Só adicionar se houver texto
                    todo = TodoItem(
                        texto=todo_data['texto'],
                        completed=todo_data.get('completed', False),
                        task_id=task.id
                    )
                    if todo_data.get('completed'):
                        todo.completed_at = datetime.utcnow()
                    db.session.add(todo)
        
        db.session.commit()
        
        # Enviar notificações por email conforme apropriado
        if task.assigned_user_id:
            usuario = User.query.get(task.assigned_user_id)
            projeto = task.project
            
            if usuario and projeto:
                try:
                    # Notificar sobre mudança de status
                    if status_mudou:
                        enviar_email_mudanca_status(usuario, task, projeto, status_antigo, task.status)
                    
                    # Notificar sobre mudança de data
                    elif data_mudou:
                        enviar_email_alteracao_data(usuario, task, projeto, data_antigo, task.data_conclusao)
                    
                    # Notificar sobre edição geral (título ou descrição)
                    elif titulo_mudou or descricao_mudou:
                        enviar_email_tarefa_editada(usuario, task, projeto)
                        
                except Exception as e:
                    app.logger.error(f"Erro ao enviar email de atualização: {e}")
        
        # Retornar dados completos da tarefa atualizada para atualizar o card
        response_data = {
            'success': True,
            'message': 'Tarefa atualizada com sucesso!',
            'task': {
                'id': task.id,
                'titulo': task.titulo,
                'status': task.status,
                'assigned_user_id': task.assigned_user_id,
                'assigned_user_name': task.assigned_user.full_name if task.assigned_user else None,
                'data_conclusao': task.data_conclusao.strftime('%d/%m/%Y') if task.data_conclusao else None,
                'data_conclusao_iso': task.data_conclusao.isoformat() if task.data_conclusao else None,
                'completed_at': task.completed_at.strftime('%d/%m/%Y às %H:%M') if task.completed_at else None,
                'project_client_name': task.project.client.nome if task.project and task.project.client else None,
                'project_name': task.project.nome if task.project else None
            }
        }
        return jsonify(response_data)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao atualizar tarefa: {str(e)}'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    try:
        # Deletar todos os to-do's relacionados primeiro
        TodoItem.query.filter_by(task_id=task.id).delete()
        
        # Deletar a tarefa
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Tarefa deletada com sucesso!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao deletar tarefa: {str(e)}'})

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
        status_antigo = task.status
        task.status = new_status
        
        if new_status == 'concluida':
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None
            
        db.session.commit()
        
        # Enviar notificação de mudança de status
        if task.assigned_user_id and status_antigo != new_status:
            usuario = User.query.get(task.assigned_user_id)
            projeto = task.project
            
            if usuario and projeto:
                try:
                    enviar_email_mudanca_status(usuario, task, projeto, status_antigo, new_status)
                except Exception as e:
                    app.logger.error(f"Erro ao enviar email de mudança de status: {e}")
        
        return jsonify({'success': True})
    
    return jsonify({'error': 'Status inválido'}), 400

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@login_required
def api_update_todo(todo_id):
    """Atualizar o texto de um to-do específico"""
    todo = TodoItem.query.get_or_404(todo_id)
    
    # Verificar permissão (usuário deve ter acesso à tarefa)
    task = todo.task
    if not current_user.is_admin and task.assigned_user_id != current_user.id:
        project = task.project
        if current_user.id != project.responsible_id and current_user not in project.team_members:
            return jsonify({'error': 'Sem permissão'}), 403
    
    data = request.get_json()
    novo_texto = data.get('texto', '').strip()
    
    if not novo_texto:
        return jsonify({'success': False, 'message': 'Texto não pode ser vazio'}), 400
    
    try:
        todo.texto = novo_texto
        db.session.commit()
        return jsonify({'success': True, 'message': 'To-do atualizado com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao atualizar: {str(e)}'}), 500

@app.route('/api/tasks/<int:task_id>/dispatch', methods=['POST'])
@login_required
def dispatch_task(task_id):
    # Apenas admin pode disparar tarefas
    if not current_user.is_admin:
        return jsonify({'error': 'Sem permissão'}), 403
    
    task = Task.query.get_or_404(task_id)
    
    # Alternar estado de disparada
    task.disparada = not task.disparada
    if task.disparada:
        task.disparada_at = datetime.utcnow()
    else:
        task.disparada_at = None
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'disparada': task.disparada,
        'disparada_at': task.disparada_at.strftime('%d/%m/%Y %H:%M') if task.disparada_at else None
    })

@app.route('/api/disparar-tarefas', methods=['POST'])
@login_required
def disparar_tarefas_filtradas():
    """Dispara emails de resumo de tarefas baseado nos filtros"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Sem permissão'}), 403
    
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        client_id = data.get('client_id')
        user_id = data.get('user_id')
        my_tasks = data.get('my_tasks', False)
        
        # Aplicar os mesmos filtros do Kanban
        query = Task.query
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        if client_id:
            query = query.join(Project).filter(Project.client_id == client_id)
        
        if user_id:
            query = query.filter_by(assigned_user_id=user_id)
        
        tasks = query.all()
        
        # Agrupar tarefas por usuário
        tarefas_por_usuario = {}
        for task in tasks:
            if task.assigned_user_id:
                if task.assigned_user_id not in tarefas_por_usuario:
                    tarefas_por_usuario[task.assigned_user_id] = []
                tarefas_por_usuario[task.assigned_user_id].append(task)
        
        # Construir informação sobre filtros aplicados
        filtro_info = ""
        if project_id:
            projeto = Project.query.get(project_id)
            filtro_info = f" do projeto '{projeto.nome}'"
        elif client_id:
            cliente = Client.query.get(client_id)
            filtro_info = f" do cliente '{cliente.nome}'"
        
        # Enviar emails
        emails_enviados = 0
        usuarios_notificados = []
        
        for usuario_id, tarefas in tarefas_por_usuario.items():
            usuario = User.query.get(usuario_id)
            if usuario and enviar_email_resumo_tarefas(usuario, tarefas, filtro_info):
                emails_enviados += 1
                usuarios_notificados.append(usuario.full_name)
        
        if emails_enviados == 0:
            return jsonify({
                'success': False,
                'message': 'Nenhum email foi enviado. Verifique se os usuários têm notificações ativadas.'
            })
        
        return jsonify({
            'success': True,
            'message': f'{emails_enviados} email(s) enviado(s) com sucesso!',
            'emails_enviados': emails_enviados,
            'usuarios': usuarios_notificados
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao enviar emails: {str(e)}'
        }), 500

@app.route('/api/projects/<int:client_id>')
@login_required
def get_projects_by_client(client_id):
    projects = Project.query.filter_by(client_id=client_id).order_by(Project.nome).all()
    project_list = [{'id': p.id, 'nome': p.nome} for p in projects]
    return jsonify(project_list)

@app.route('/kanban/transcription', methods=['POST'])
@login_required
def kanban_transcription():
    data = request.get_json()
    
    try:
        project_id = data.get('project_id')
        transcription = data.get('transcription')
        
        if not project_id or not transcription:
            return jsonify({'success': False, 'message': 'Dados incompletos'})
        
        project = Project.query.get_or_404(project_id)
        
        # Gerar tarefas com IA usando a transcrição
        auto_tasks = generate_tasks_from_transcription(transcription, project.nome)
        
        tasks_created = 0
        for task_data in auto_tasks:
            task = Task(
                titulo=task_data['titulo'],
                descricao=task_data['descricao'],
                project_id=project.id,
                status='pendente'
            )
            db.session.add(task)
            tasks_created += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{tasks_created} tarefas foram geradas com sucesso!',
            'tasks_created': tasks_created
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao processar transcrição: {e}")
        return jsonify({
            'success': False, 
            'message': 'Erro ao processar a transcrição. Tente novamente mais tarde.'
        })

# Rotas para redefinição de senha
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Gerar token de reset
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)  # Token expira em 1 hora
            db.session.commit()
            
            # Por enquanto vamos apenas mostrar uma mensagem de confirmação
            # Em uma implementação real, aqui seria enviado um email
            flash(f'Um link de redefinição de senha foi gerado. Use este link para redefinir sua senha: /reset-password/{token}', 'info')
        else:
            # Por segurança, não revelamos se o email existe ou não
            flash('Se o email estiver cadastrado, você receberá instruções para redefinir sua senha.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Encontrar usuário pelo token
    user = User.query.filter(
        User.reset_token == token,
        User.reset_token_expires > datetime.utcnow()
    ).first()
    
    if not user:
        flash('Token de redefinição inválido ou expirado.', 'danger')
        return redirect(url_for('forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        
        flash('Sua senha foi redefinida com sucesso! Faça login com sua nova senha.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('Senha atual incorreta.', 'danger')
            return render_template('change_password.html', form=form)
        
        current_user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()
        
        flash('Sua senha foi alterada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('change_password.html', form=form)

# Rotas para exportar/importar dados
@app.route('/admin/export-data')
@login_required
def export_database():
    """Exporta todos os dados do banco para download"""
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem exportar dados.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        export_data = {
            'export_date': datetime.now().isoformat(),
            'exported_by': current_user.email,
            'users': [],
            'clients': [],
            'projects': [],
            'tasks': [],
            'todos': []
        }
        
        # Exportar usuários
        users = User.query.all()
        for user in users:
            export_data['users'].append({
                'id': user.id,
                'nome': user.nome,
                'sobrenome': user.sobrenome,
                'email': user.email,
                'password_hash': user.password_hash,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        # Exportar clientes
        clients = Client.query.all()
        for client in clients:
            export_data['clients'].append({
                'id': client.id,
                'nome': client.nome,
                'email': client.email,
                'telefone': client.telefone,
                'endereco': client.endereco,
                'public_code': client.public_code,
                'creator_id': client.creator_id,
                'created_at': client.created_at.isoformat() if client.created_at else None
            })
        
        # Exportar projetos
        projects = Project.query.order_by(Project.nome).all()
        for project in projects:
            team_member_ids = [member.id for member in project.team_members]
            export_data['projects'].append({
                'id': project.id,
                'nome': project.nome,
                'transcricao': project.transcricao,
                'status': project.status,
                'client_id': project.client_id,
                'responsible_id': project.responsible_id,
                'team_member_ids': team_member_ids,
                'contexto_justificativa': project.contexto_justificativa,
                'descricao_resumida': project.descricao_resumida,
                'problema_oportunidade': project.problema_oportunidade,
                'objetivos': project.objetivos,
                'alinhamento_estrategico': project.alinhamento_estrategico,
                'escopo_projeto': project.escopo_projeto,
                'fora_escopo': project.fora_escopo,
                'premissas': project.premissas,
                'restricoes': project.restricoes,
                'created_at': project.created_at.isoformat() if project.created_at else None
            })
        
        # Exportar tarefas
        tasks = Task.query.all()
        for task in tasks:
            export_data['tasks'].append({
                'id': task.id,
                'titulo': task.titulo,
                'descricao': task.descricao,
                'status': task.status,
                'project_id': task.project_id,
                'assigned_user_id': task.assigned_user_id,
                'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None
            })
        
        # Exportar todos
        todos = TodoItem.query.all()
        for todo in todos:
            export_data['todos'].append({
                'id': todo.id,
                'texto': todo.texto,
                'completed': todo.completed,
                'task_id': todo.task_id,
                'created_at': todo.created_at.isoformat() if todo.created_at else None,
                'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
            })
        
        # Criar resposta JSON para download
        response = jsonify(export_data)
        response.headers['Content-Disposition'] = f'attachment; filename=database_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        response.headers['Content-Type'] = 'application/json'
        
        flash(f'Dados exportados com sucesso! {len(export_data["users"])} usuários, {len(export_data["clients"])} clientes, {len(export_data["projects"])} projetos, {len(export_data["tasks"])} tarefas e {len(export_data["todos"])} todos.', 'success')
        
        return response
        
    except Exception as e:
        flash(f'Erro ao exportar dados: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/admin/import-data', methods=['GET', 'POST'])
@login_required
def import_database():
    """Página para importar dados"""
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem importar dados.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'data_file' not in request.files:
            flash('Nenhum arquivo foi selecionado.', 'danger')
            return render_template('import_data.html')
        
        file = request.files['data_file']
        if file.filename == '':
            flash('Nenhum arquivo foi selecionado.', 'danger')
            return render_template('import_data.html')
        
        if file and file.filename.endswith('.json'):
            try:
                # Ler conteúdo do arquivo
                content = file.read().decode('utf-8')
                data = json.loads(content)
                
                # Validar estrutura básica
                required_keys = ['users', 'clients', 'projects', 'tasks', 'todos']
                if not all(key in data for key in required_keys):
                    flash('Arquivo JSON inválido. Estrutura incorreta.', 'danger')
                    return render_template('import_data.html')
                
                # Importar dados
                user_id_map = {}
                client_id_map = {}
                project_id_map = {}
                task_id_map = {}
                
                stats = {'users': 0, 'clients': 0, 'projects': 0, 'tasks': 0, 'todos': 0}
                
                # Importar usuários
                for user_data in data['users']:
                    existing_user = User.query.filter_by(email=user_data['email']).first()
                    if not existing_user:
                        user = User(
                            nome=user_data['nome'],
                            sobrenome=user_data['sobrenome'],
                            email=user_data['email'],
                            password_hash=user_data['password_hash'],
                            is_admin=user_data['is_admin'],
                            created_at=datetime.fromisoformat(user_data['created_at']) if user_data['created_at'] else datetime.now()
                        )
                        db.session.add(user)
                        db.session.flush()
                        stats['users'] += 1
                        user_id_map[user_data['id']] = user.id
                    else:
                        user_id_map[user_data['id']] = existing_user.id
                
                # Importar clientes
                for client_data in data['clients']:
                    existing_client = Client.query.filter_by(nome=client_data['nome']).first()
                    if not existing_client:
                        client = Client(
                            nome=client_data['nome'],
                            email=client_data['email'],
                            telefone=client_data['telefone'],
                            endereco=client_data['endereco'],
                            public_code=client_data['public_code'],
                            creator_id=user_id_map.get(client_data['creator_id'], current_user.id),
                            created_at=datetime.fromisoformat(client_data['created_at']) if client_data['created_at'] else datetime.now()
                        )
                        db.session.add(client)
                        db.session.flush()
                        stats['clients'] += 1
                        client_id_map[client_data['id']] = client.id
                    else:
                        client_id_map[client_data['id']] = existing_client.id
                
                # Importar projetos
                for project_data in data['projects']:
                    existing_project = Project.query.filter_by(nome=project_data['nome']).first()
                    if not existing_project and client_id_map.get(project_data['client_id']):
                        project = Project(
                            nome=project_data['nome'],
                            transcricao=project_data.get('transcricao'),
                            status=project_data['status'],
                            client_id=client_id_map[project_data['client_id']],
                            responsible_id=user_id_map.get(project_data['responsible_id']),
                            contexto_justificativa=project_data.get('contexto_justificativa'),
                            descricao_resumida=project_data.get('descricao_resumida'),
                            problema_oportunidade=project_data.get('problema_oportunidade'),
                            objetivos=project_data.get('objetivos'),
                            alinhamento_estrategico=project_data.get('alinhamento_estrategico'),
                            escopo_projeto=project_data.get('escopo_projeto'),
                            fora_escopo=project_data.get('fora_escopo'),
                            premissas=project_data.get('premissas'),
                            restricoes=project_data.get('restricoes'),
                            created_at=datetime.fromisoformat(project_data['created_at']) if project_data['created_at'] else datetime.now()
                        )
                        db.session.add(project)
                        db.session.flush()
                        
                        # Adicionar membros da equipe
                        for old_member_id in project_data.get('team_member_ids', []):
                            new_member_id = user_id_map.get(old_member_id)
                            if new_member_id:
                                member = User.query.get(new_member_id)
                                if member:
                                    project.team_members.append(member)
                        
                        stats['projects'] += 1
                        project_id_map[project_data['id']] = project.id
                    elif existing_project:
                        project_id_map[project_data['id']] = existing_project.id
                
                # Importar tarefas
                for task_data in data['tasks']:
                    project_id = project_id_map.get(task_data['project_id'])
                    if project_id:
                        # Verificar se tarefa já existe
                        existing_task = Task.query.filter_by(
                            titulo=task_data['titulo'], 
                            project_id=project_id
                        ).first()
                        
                        if not existing_task:
                            task = Task(
                                titulo=task_data['titulo'],
                                descricao=task_data['descricao'],
                                status=task_data['status'],
                                project_id=project_id,
                                assigned_user_id=user_id_map.get(task_data['assigned_user_id']) if task_data['assigned_user_id'] else None,
                                data_conclusao=datetime.fromisoformat(task_data['data_conclusao']).date() if task_data['data_conclusao'] else None,
                                created_at=datetime.fromisoformat(task_data['created_at']) if task_data['created_at'] else datetime.now(),
                                completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data['completed_at'] else None
                            )
                            db.session.add(task)
                            db.session.flush()
                            stats['tasks'] += 1
                            task_id_map[task_data['id']] = task.id
                        else:
                            task_id_map[task_data['id']] = existing_task.id
                
                # Importar todos (to-do items)
                for todo_data in data['todos']:
                    task_id = task_id_map.get(todo_data['task_id'])
                    if task_id:
                        # Verificar se todo já existe
                        existing_todo = TodoItem.query.filter_by(
                            texto=todo_data['texto'], 
                            task_id=task_id
                        ).first()
                        
                        if not existing_todo:
                            todo = TodoItem(
                                texto=todo_data['texto'],
                                completed=todo_data['completed'],
                                task_id=task_id,
                                created_at=datetime.fromisoformat(todo_data['created_at']) if todo_data['created_at'] else datetime.now(),
                                completed_at=datetime.fromisoformat(todo_data['completed_at']) if todo_data['completed_at'] else None
                            )
                            db.session.add(todo)
                            stats['todos'] += 1
                
                db.session.commit()
                
                flash(f'Importação concluída! {stats["users"]} usuários, {stats["clients"]} clientes, {stats["projects"]} projetos, {stats["tasks"]} tarefas e {stats["todos"]} todos importados.', 'success')
                return redirect(url_for('dashboard'))
                
            except json.JSONDecodeError:
                flash('Erro: arquivo JSON inválido.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao importar dados: {str(e)}', 'danger')
        else:
            flash('Por favor, selecione um arquivo JSON válido.', 'danger')
    
    return render_template('import_data.html')

# Rotas específicas para tarefas
@app.route('/admin/export-tasks')
@login_required
def export_tasks():
    """Exporta apenas tarefas e todos para download"""
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem exportar tarefas.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        export_data = {
            'export_date': datetime.now().isoformat(),
            'exported_by': current_user.email,
            'export_type': 'tasks_only',
            'tasks': [],
            'todos': [],
            'projects_reference': [],
            'users_reference': []
        }
        
        # Exportar tarefas
        tasks = Task.query.all()
        for task in tasks:
            export_data['tasks'].append({
                'id': task.id,
                'titulo': task.titulo,
                'descricao': task.descricao,
                'status': task.status,
                'project_id': task.project_id,
                'project_name': task.project.nome if task.project else None,
                'client_name': task.project.client.nome if task.project and task.project.client else None,
                'assigned_user_id': task.assigned_user_id,
                'assigned_user_name': task.assigned_user.full_name if task.assigned_user else None,
                'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None
            })
        
        # Exportar todos
        todos = TodoItem.query.all()
        for todo in todos:
            export_data['todos'].append({
                'id': todo.id,
                'texto': todo.texto,
                'completed': todo.completed,
                'task_id': todo.task_id,
                'task_title': todo.task.titulo if todo.task else None,
                'created_at': todo.created_at.isoformat() if todo.created_at else None,
                'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
            })
        
        # Adicionar projetos e usuários como referência para importação
        projects = Project.query.order_by(Project.nome).all()
        for project in projects:
            export_data['projects_reference'].append({
                'id': project.id,
                'nome': project.nome,
                'client_name': project.client.nome if project.client else None
            })
        
        users = User.query.filter_by(is_admin=False).all()
        for user in users:
            export_data['users_reference'].append({
                'id': user.id,
                'nome': user.full_name,
                'email': user.email
            })
        
        # Criar resposta JSON para download
        response = jsonify(export_data)
        response.headers['Content-Disposition'] = f'attachment; filename=tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        response.headers['Content-Type'] = 'application/json'
        
        flash(f'Tarefas exportadas com sucesso! {len(export_data["tasks"])} tarefas e {len(export_data["todos"])} todos.', 'success')
        
        return response
        
    except Exception as e:
        flash(f'Erro ao exportar tarefas: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/admin/import-tasks', methods=['GET', 'POST'])
@login_required
def import_tasks():
    """Página para importar apenas tarefas"""
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem importar tarefas.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'data_file' not in request.files:
            flash('Nenhum arquivo foi selecionado.', 'danger')
            return render_template('import_tasks.html')
        
        file = request.files['data_file']
        if file.filename == '':
            flash('Nenhum arquivo foi selecionado.', 'danger')
            return render_template('import_tasks.html')
        
        if file and file.filename.endswith('.json'):
            try:
                # Ler conteúdo do arquivo
                content = file.read().decode('utf-8')
                data = json.loads(content)
                
                # Validar se é arquivo de tarefas
                if data.get('export_type') != 'tasks_only':
                    flash('Este arquivo não é um export específico de tarefas. Use a importação completa de dados.', 'warning')
                    return render_template('import_tasks.html')
                
                # Validar estrutura básica
                required_keys = ['tasks', 'todos']
                if not all(key in data for key in required_keys):
                    flash('Arquivo JSON inválido. Estrutura incorreta para importação de tarefas.', 'danger')
                    return render_template('import_tasks.html')
                
                # Mapear IDs para importação
                task_id_map = {}
                stats = {'tasks': 0, 'todos': 0, 'skipped_tasks': 0}
                
                # Importar tarefas
                for task_data in data['tasks']:
                    # Verificar se o projeto existe
                    project = None
                    if task_data.get('project_id'):
                        project = Project.query.get(task_data['project_id'])
                    
                    # Se projeto não existe, tentar encontrar por nome
                    if not project and task_data.get('project_name'):
                        project = Project.query.filter_by(nome=task_data['project_name']).first()
                    
                    if not project:
                        stats['skipped_tasks'] += 1
                        continue
                    
                    # Verificar se tarefa já existe
                    existing_task = Task.query.filter_by(
                        titulo=task_data['titulo'], 
                        project_id=project.id
                    ).first()
                    
                    if not existing_task:
                        # Encontrar usuário responsável
                        assigned_user = None
                        if task_data.get('assigned_user_id'):
                            assigned_user = User.query.get(task_data['assigned_user_id'])
                        elif task_data.get('assigned_user_name'):
                            # Tentar encontrar por nome
                            for user in User.query.filter_by(is_admin=False).all():
                                if user.full_name == task_data['assigned_user_name']:
                                    assigned_user = user
                                    break
                        
                        task = Task(
                            titulo=task_data['titulo'],
                            descricao=task_data['descricao'],
                            status=task_data['status'],
                            project_id=project.id,
                            assigned_user_id=assigned_user.id if assigned_user else None,
                            data_conclusao=datetime.fromisoformat(task_data['data_conclusao']).date() if task_data['data_conclusao'] else None,
                            created_at=datetime.fromisoformat(task_data['created_at']) if task_data['created_at'] else datetime.now(),
                            completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data['completed_at'] else None
                        )
                        db.session.add(task)
                        db.session.flush()
                        stats['tasks'] += 1
                        task_id_map[task_data['id']] = task.id
                    else:
                        task_id_map[task_data['id']] = existing_task.id
                
                # Importar todos (to-do items)
                for todo_data in data['todos']:
                    task_id = task_id_map.get(todo_data['task_id'])
                    if task_id:
                        # Verificar se todo já existe
                        existing_todo = TodoItem.query.filter_by(
                            texto=todo_data['texto'], 
                            task_id=task_id
                        ).first()
                        
                        if not existing_todo:
                            todo = TodoItem(
                                texto=todo_data['texto'],
                                completed=todo_data['completed'],
                                task_id=task_id,
                                created_at=datetime.fromisoformat(todo_data['created_at']) if todo_data['created_at'] else datetime.now(),
                                completed_at=datetime.fromisoformat(todo_data['completed_at']) if todo_data['completed_at'] else None
                            )
                            db.session.add(todo)
                            stats['todos'] += 1
                
                db.session.commit()
                
                message = f'Importação de tarefas concluída! {stats["tasks"]} tarefas e {stats["todos"]} todos importados.'
                if stats['skipped_tasks'] > 0:
                    message += f' {stats["skipped_tasks"]} tarefas foram ignoradas (projeto não encontrado).'
                
                flash(message, 'success')
                return redirect(url_for('dashboard'))
                
            except json.JSONDecodeError:
                flash('Erro: arquivo JSON inválido.', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao importar tarefas: {str(e)}', 'danger')
        else:
            flash('Por favor, selecione um arquivo JSON válido.', 'danger')
    
    return render_template('import_tasks.html')
