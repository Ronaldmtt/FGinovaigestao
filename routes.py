from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import httpx
from app import app, db
from models import User, Client, Project, Task, TodoItem
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
    form = ClientForm()
    return render_template('clients.html', clients=clients, form=form)

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
    
    form = ProjectForm()
    return render_template('projects.html', projects=projects, form=form)

@app.route('/projects/new', methods=['GET', 'POST'])
@login_required
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
    
    return render_template('projects.html', form=form)

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
    
    # Adicionar membro da equipe se selecionado
    team_member_id = request.form.get('team_member_id')
    if team_member_id:
        user = User.query.get(team_member_id)
        if user and user not in project.team_members:
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
def tasks():
    if current_user.is_admin:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(assigned_user_id=current_user.id).all()
    
    form = TaskForm()
    transcription_form = TranscriptionTaskForm()
    return render_template('tasks.html', tasks=tasks, form=form, transcription_form=transcription_form)

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
    
    # Todos os usuários para o modal de edição
    all_users = User.query.filter_by(is_admin=False).all()
    
    return render_template('kanban.html', 
                         task_columns=task_columns, 
                         projects=projects, 
                         clients=clients,
                         all_users=all_users,
                         current_filters={
                             'project_id': project_filter,
                             'client_id': client_filter,
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
    
    try:
        # Atualizar campos
        if 'titulo' in data:
            task.titulo = data['titulo']
        if 'descricao' in data:
            task.descricao = data['descricao']
        if 'assigned_user_id' in data:
            task.assigned_user_id = data['assigned_user_id'] if data['assigned_user_id'] else None
        if 'status' in data:
            task.status = data['status']
            # Atualizar data de conclusão baseado no status
            if data['status'] == 'concluida':
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        if 'data_conclusao' in data:
            if data['data_conclusao']:
                task.data_conclusao = datetime.strptime(data['data_conclusao'], '%Y-%m-%d').date()
            else:
                task.data_conclusao = None
        
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
        return jsonify({'success': True, 'message': 'Tarefa atualizada com sucesso!'})
        
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
