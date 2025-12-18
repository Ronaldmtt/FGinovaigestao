"""
API v1 - Autenticação por API Key (Project-scoped + User-scoped)
"""
import secrets
import json
from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

from app import db
from models import Project, Task, TodoItem, User, ProjectApiKey, SystemApiKey, Client

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


def api_error(code, message, status_code=400):
    """Retorna erro padronizado"""
    return jsonify({
        'error': {
            'code': code,
            'message': message
        }
    }), status_code


def require_project_api_key(required_scopes=None):
    """
    Decorator para autenticação via API Key.
    - Lê Authorization: Bearer <token> ou X-API-Key: <token>
    - Valida prefix, hash, ativo, scopes
    - Seta g.api_key, g.api_user, g.api_project
    - Atualiza last_used_at
    """
    if required_scopes is None:
        required_scopes = []
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]
            
            if not token:
                token = request.headers.get('X-API-Key')
            
            if not token:
                return api_error('missing_api_key', 'API Key não fornecida. Use Authorization: Bearer <token> ou X-API-Key: <token>', 401)
            
            if len(token) < 10:
                return api_error('invalid_api_key', 'API Key inválida', 401)
            
            prefix = token[:10]
            api_key = ProjectApiKey.query.filter_by(prefix=prefix).first()
            
            if not api_key:
                return api_error('invalid_api_key', 'API Key não encontrada', 401)
            
            if not check_password_hash(api_key.key_hash, token):
                return api_error('invalid_api_key', 'API Key inválida', 401)
            
            if not api_key.is_active():
                if api_key.revoked_at:
                    return api_error('api_key_revoked', 'Esta API Key foi revogada', 401)
                else:
                    return api_error('api_key_expired', 'Esta API Key expirou', 401)
            
            for scope in required_scopes:
                if not api_key.has_scope(scope):
                    return api_error('insufficient_scope', f'Permissão insuficiente. Escopo necessário: {scope}', 403)
            
            api_key.last_used_at = datetime.utcnow()
            db.session.commit()
            
            g.api_key = api_key
            g.api_user = api_key.user
            g.api_project = api_key.project
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_system_api_key(required_scopes=None):
    """
    Decorator para autenticação via System API Key (acesso geral ao sistema).
    - Lê Authorization: Bearer <token> ou X-API-Key: <token>
    - Valida prefix, hash, ativo, scopes
    - Seta g.api_key, g.api_user
    - Atualiza last_used_at
    """
    if required_scopes is None:
        required_scopes = []
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]
            
            if not token:
                token = request.headers.get('X-API-Key')
            
            if not token:
                return api_error('missing_api_key', 'API Key não fornecida. Use Authorization: Bearer <token> ou X-API-Key: <token>', 401)
            
            if len(token) < 10:
                return api_error('invalid_api_key', 'API Key inválida', 401)
            
            prefix = token[:10]
            api_key = SystemApiKey.query.filter_by(prefix=prefix).first()
            
            if not api_key:
                return api_error('invalid_api_key', 'API Key não encontrada ou não é uma chave de sistema', 401)
            
            if not check_password_hash(api_key.key_hash, token):
                return api_error('invalid_api_key', 'API Key inválida', 401)
            
            if not api_key.is_active():
                if api_key.revoked_at:
                    return api_error('api_key_revoked', 'Esta API Key foi revogada', 401)
                else:
                    return api_error('api_key_expired', 'Esta API Key expirou', 401)
            
            for scope in required_scopes:
                if not api_key.has_scope(scope):
                    return api_error('insufficient_scope', f'Permissão insuficiente. Escopo necessário: {scope}', 403)
            
            api_key.last_used_at = datetime.utcnow()
            db.session.commit()
            
            g.api_key = api_key
            g.api_user = api_key.user
            g.is_system_key = True
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_task_belongs_to_project(task_id):
    """Valida que a task pertence ao projeto da API key (anti-IDOR)"""
    task = Task.query.get(task_id)
    if not task:
        return None, api_error('task_not_found', 'Tarefa não encontrada', 404)
    if task.project_id != g.api_project.id:
        return None, api_error('access_denied', 'Tarefa não pertence a este projeto', 403)
    return task, None


def validate_todo_belongs_to_project(todo_id):
    """Valida que o todo pertence ao projeto da API key (anti-IDOR)"""
    todo = TodoItem.query.get(todo_id)
    if not todo:
        return None, api_error('todo_not_found', 'Subtarefa não encontrada', 404)
    if todo.task.project_id != g.api_project.id:
        return None, api_error('access_denied', 'Subtarefa não pertence a este projeto', 403)
    return todo, None


@api_v1.route('/project', methods=['GET'])
@require_project_api_key(required_scopes=['projects:read'])
def get_project():
    """Retorna o projeto associado à API key"""
    project = g.api_project
    return jsonify({
        'success': True,
        'project': {
            'id': project.id,
            'nome': project.nome,
            'status': project.status,
            'progress_percent': project.progress_percent,
            'prazo': project.prazo.isoformat() if project.prazo else None,
            'created_at': project.created_at.isoformat() if project.created_at else None,
            'descricao_resumida': project.descricao_resumida,
            'objetivos': project.objetivos,
            'client': {
                'id': project.client.id,
                'nome': project.client.nome
            } if project.client else None,
            'responsible': {
                'id': project.responsible.id,
                'nome': project.responsible.full_name
            } if project.responsible else None
        }
    })


@api_v1.route('/tasks', methods=['GET'])
@require_project_api_key(required_scopes=['tasks:read'])
def list_tasks():
    """Lista tarefas do projeto com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 200)
    status = request.args.get('status')
    assigned_user_id = request.args.get('assigned_user_id', type=int)
    
    query = Task.query.filter_by(project_id=g.api_project.id)
    
    if status:
        query = query.filter_by(status=status)
    if assigned_user_id:
        query = query.filter_by(assigned_user_id=assigned_user_id)
    
    query = query.order_by(Task.ordem, Task.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    tasks = []
    for task in pagination.items:
        tasks.append({
            'id': task.id,
            'titulo': task.titulo,
            'descricao': task.descricao,
            'status': task.status,
            'ordem': task.ordem,
            'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'assigned_user': {
                'id': task.assigned_user.id,
                'nome': task.assigned_user.full_name
            } if task.assigned_user else None,
            'todos_count': len(task.todos),
            'todos_completed': len([t for t in task.todos if t.completed])
        })
    
    return jsonify({
        'success': True,
        'tasks': tasks,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@api_v1.route('/tasks', methods=['POST'])
@require_project_api_key(required_scopes=['tasks:write'])
def create_task():
    """Cria uma nova tarefa no projeto"""
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'Body JSON inválido', 400)
    
    titulo = data.get('titulo')
    if not titulo or not titulo.strip():
        return api_error('missing_field', 'Campo titulo é obrigatório', 400)
    
    max_ordem = db.session.query(db.func.max(Task.ordem)).filter_by(
        project_id=g.api_project.id, status='pendente'
    ).scalar() or 0
    
    task = Task(
        titulo=titulo.strip(),
        descricao=data.get('descricao', ''),
        status=data.get('status', 'pendente'),
        project_id=g.api_project.id,
        ordem=max_ordem + 1
    )
    
    if data.get('data_conclusao'):
        try:
            task.data_conclusao = datetime.fromisoformat(data['data_conclusao']).date()
        except:
            pass
    
    assigned_user_id = data.get('assigned_user_id')
    if assigned_user_id:
        user = User.query.get(assigned_user_id)
        if user:
            project = g.api_project
            is_authorized = (
                user.id == project.responsible_id or
                user in project.team_members or
                user.is_admin
            )
            if is_authorized:
                task.assigned_user_id = user.id
            else:
                return api_error('invalid_user', 'Usuário não faz parte deste projeto', 400)
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': {
            'id': task.id,
            'titulo': task.titulo,
            'descricao': task.descricao,
            'status': task.status,
            'ordem': task.ordem,
            'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
            'created_at': task.created_at.isoformat() if task.created_at else None
        }
    }), 201


@api_v1.route('/tasks/<int:task_id>/update', methods=['POST'])
@require_project_api_key(required_scopes=['tasks:write'])
def update_task(task_id):
    """Atualiza uma tarefa (whitelist de campos permitidos)"""
    task, error = validate_task_belongs_to_project(task_id)
    if error:
        return error
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'Body JSON inválido', 400)
    
    allowed_fields = ['titulo', 'descricao', 'assigned_user_id', 'data_conclusao', 'ordem']
    
    for field in allowed_fields:
        if field in data:
            if field == 'titulo':
                if data[field] and data[field].strip():
                    task.titulo = data[field].strip()
            elif field == 'descricao':
                task.descricao = data.get(field, '')
            elif field == 'assigned_user_id':
                if data[field] is None:
                    task.assigned_user_id = None
                else:
                    user = User.query.get(data[field])
                    if user:
                        project = g.api_project
                        is_authorized = (
                            user.id == project.responsible_id or
                            user in project.team_members or
                            user.is_admin
                        )
                        if is_authorized:
                            task.assigned_user_id = user.id
                        else:
                            return api_error('invalid_user', 'Usuário não faz parte deste projeto', 400)
            elif field == 'data_conclusao':
                if data[field]:
                    try:
                        task.data_conclusao = datetime.fromisoformat(data[field]).date()
                    except:
                        pass
                else:
                    task.data_conclusao = None
            elif field == 'ordem':
                if isinstance(data[field], int):
                    task.ordem = data[field]
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': {
            'id': task.id,
            'titulo': task.titulo,
            'descricao': task.descricao,
            'status': task.status,
            'ordem': task.ordem,
            'data_conclusao': task.data_conclusao.isoformat() if task.data_conclusao else None,
            'assigned_user_id': task.assigned_user_id
        }
    })


@api_v1.route('/tasks/<int:task_id>/status', methods=['POST'])
@require_project_api_key(required_scopes=['tasks:write'])
def update_task_status(task_id):
    """Atualiza o status/coluna de uma tarefa"""
    task, error = validate_task_belongs_to_project(task_id)
    if error:
        return error
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'Body JSON inválido', 400)
    
    new_status = data.get('status')
    valid_statuses = ['pendente', 'em_andamento', 'concluida']
    
    if new_status not in valid_statuses:
        return api_error('invalid_status', f'Status inválido. Use: {", ".join(valid_statuses)}', 400)
    
    old_status = task.status
    task.status = new_status
    
    if new_status == 'concluida' and old_status != 'concluida':
        task.completed_at = datetime.utcnow()
    elif new_status != 'concluida':
        task.completed_at = None
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': {
            'id': task.id,
            'status': task.status,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None
        }
    })


@api_v1.route('/tasks/reorder', methods=['POST'])
@require_project_api_key(required_scopes=['tasks:write'])
def reorder_tasks():
    """Reordena tarefas do projeto"""
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'Body JSON inválido', 400)
    
    task_ids = data.get('task_ids', [])
    if not isinstance(task_ids, list):
        return api_error('invalid_field', 'task_ids deve ser uma lista', 400)
    
    for idx, task_id in enumerate(task_ids):
        task = Task.query.get(task_id)
        if not task:
            return api_error('task_not_found', f'Tarefa {task_id} não encontrada', 404)
        if task.project_id != g.api_project.id:
            return api_error('access_denied', f'Tarefa {task_id} não pertence a este projeto', 403)
        task.ordem = idx
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{len(task_ids)} tarefas reordenadas'
    })


@api_v1.route('/tasks/<int:task_id>', methods=['DELETE'])
@require_project_api_key(required_scopes=['tasks:write'])
def delete_task(task_id):
    """Deleta uma tarefa"""
    task, error = validate_task_belongs_to_project(task_id)
    if error:
        return error
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Tarefa deletada com sucesso'
    })


@api_v1.route('/tasks/<int:task_id>/todos', methods=['GET'])
@require_project_api_key(required_scopes=['tasks:read'])
def list_todos(task_id):
    """Lista subtarefas de uma tarefa"""
    task, error = validate_task_belongs_to_project(task_id)
    if error:
        return error
    
    todos = TodoItem.query.filter_by(task_id=task_id).order_by(
        TodoItem.completed, TodoItem.created_at
    ).all()
    
    return jsonify({
        'success': True,
        'todos': [{
            'id': todo.id,
            'texto': todo.texto,
            'comentario': todo.comentario,
            'completed': todo.completed,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'created_at': todo.created_at.isoformat() if todo.created_at else None,
            'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
        } for todo in todos]
    })


@api_v1.route('/tasks/<int:task_id>/todos', methods=['POST'])
@require_project_api_key(required_scopes=['tasks:write'])
def create_todo(task_id):
    """Cria uma subtarefa"""
    task, error = validate_task_belongs_to_project(task_id)
    if error:
        return error
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'Body JSON inválido', 400)
    
    texto = data.get('texto')
    if not texto or not texto.strip():
        return api_error('missing_field', 'Campo texto é obrigatório', 400)
    
    todo = TodoItem(
        texto=texto.strip()[:300],
        task_id=task_id,
        comentario=data.get('comentario', '')
    )
    
    if data.get('due_date'):
        try:
            todo.due_date = datetime.fromisoformat(data['due_date']).date()
        except:
            pass
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'todo': {
            'id': todo.id,
            'texto': todo.texto,
            'comentario': todo.comentario,
            'completed': todo.completed,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'created_at': todo.created_at.isoformat() if todo.created_at else None
        }
    }), 201


@api_v1.route('/todos/<int:todo_id>', methods=['PUT'])
@require_project_api_key(required_scopes=['tasks:write'])
def update_todo(todo_id):
    """Atualiza uma subtarefa"""
    todo, error = validate_todo_belongs_to_project(todo_id)
    if error:
        return error
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'Body JSON inválido', 400)
    
    if 'texto' in data and data['texto'] and data['texto'].strip():
        todo.texto = data['texto'].strip()[:300]
    
    if 'comentario' in data:
        todo.comentario = data.get('comentario', '')
    
    if 'completed' in data:
        was_completed = todo.completed
        todo.completed = bool(data['completed'])
        if todo.completed and not was_completed:
            todo.completed_at = datetime.utcnow()
        elif not todo.completed:
            todo.completed_at = None
    
    if 'due_date' in data:
        if data['due_date']:
            try:
                todo.due_date = datetime.fromisoformat(data['due_date']).date()
            except:
                pass
        else:
            todo.due_date = None
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'todo': {
            'id': todo.id,
            'texto': todo.texto,
            'comentario': todo.comentario,
            'completed': todo.completed,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
        }
    })


@api_v1.route('/todos/<int:todo_id>', methods=['DELETE'])
@require_project_api_key(required_scopes=['tasks:write'])
def delete_todo(todo_id):
    """Deleta uma subtarefa"""
    todo, error = validate_todo_belongs_to_project(todo_id)
    if error:
        return error
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Subtarefa deletada com sucesso'
    })


@api_v1.route('/todos/<int:todo_id>/toggle', methods=['POST'])
@require_project_api_key(required_scopes=['tasks:write'])
def toggle_todo(todo_id):
    """Toggle completed de uma subtarefa"""
    todo, error = validate_todo_belongs_to_project(todo_id)
    if error:
        return error
    
    todo.completed = not todo.completed
    if todo.completed:
        todo.completed_at = datetime.utcnow()
    else:
        todo.completed_at = None
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'todo': {
            'id': todo.id,
            'completed': todo.completed,
            'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
        }
    })


def generate_api_key(project_id, user_id, name, scopes, expires_days=30):
    """
    Gera uma nova API Key para o projeto/usuário.
    Retorna o token UMA única vez (não é armazenado em texto puro).
    """
    token = secrets.token_urlsafe(32)
    prefix = token[:10]
    key_hash = generate_password_hash(token)
    
    expires_at = datetime.utcnow() + timedelta(days=expires_days) if expires_days else None
    
    api_key = ProjectApiKey(
        project_id=project_id,
        user_id=user_id,
        name=name,
        prefix=prefix,
        key_hash=key_hash,
        scopes_json=json.dumps(scopes) if scopes else '[]',
        expires_at=expires_at
    )
    
    db.session.add(api_key)
    db.session.commit()
    
    return api_key, token


def generate_system_api_key(user_id, name, scopes, expires_days=30):
    """
    Gera uma nova System API Key para acesso geral ao sistema.
    Retorna o token UMA única vez (não é armazenado em texto puro).
    """
    token = secrets.token_urlsafe(32)
    prefix = token[:10]
    key_hash = generate_password_hash(token)
    
    expires_at = datetime.utcnow() + timedelta(days=expires_days) if expires_days else None
    
    api_key = SystemApiKey(
        user_id=user_id,
        name=name,
        prefix=prefix,
        key_hash=key_hash,
        scopes_json=json.dumps(scopes) if scopes else '[]',
        expires_at=expires_at
    )
    
    db.session.add(api_key)
    db.session.commit()
    
    return api_key, token


# ============================================================================
# SYSTEM API ENDPOINTS (General access - not project-scoped)
# ============================================================================

@api_v1.route('/clients', methods=['GET'])
@require_system_api_key(required_scopes=['clients:read'])
def list_clients():
    """Lista todos os clientes"""
    clients = Client.query.order_by(Client.nome).all()
    
    return jsonify({
        'success': True,
        'clients': [{
            'id': c.id,
            'nome': c.nome,
            'email': c.email,
            'telefone': c.telefone,
            'empresa': c.empresa,
            'endereco': c.endereco,
            'observacoes': c.observacoes,
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'projects_count': len(c.projects) if c.projects else 0
        } for c in clients],
        'total': len(clients)
    })


@api_v1.route('/clients/<int:client_id>', methods=['GET'])
@require_system_api_key(required_scopes=['clients:read'])
def get_client(client_id):
    """Retorna detalhes de um cliente"""
    client = Client.query.get(client_id)
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    return jsonify({
        'success': True,
        'client': {
            'id': client.id,
            'nome': client.nome,
            'email': client.email,
            'telefone': client.telefone,
            'empresa': client.empresa,
            'endereco': client.endereco,
            'observacoes': client.observacoes,
            'created_at': client.created_at.isoformat() if client.created_at else None,
            'projects': [{
                'id': p.id,
                'nome': p.nome,
                'status': p.status
            } for p in client.projects] if client.projects else []
        }
    })


@api_v1.route('/clients', methods=['POST'])
@require_system_api_key(required_scopes=['clients:write'])
def create_client():
    """Cria um novo cliente"""
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    if not data.get('nome'):
        return api_error('missing_field', 'Campo obrigatório: nome', 400)
    
    system_api_key = g.get('system_api_key')
    creator_id = system_api_key.user_id if system_api_key else 1
    
    client = Client(
        nome=data['nome'],
        email=data.get('email'),
        telefone=data.get('telefone'),
        empresa=data.get('empresa'),
        endereco=data.get('endereco'),
        observacoes=data.get('observacoes'),
        creator_id=creator_id
    )
    
    db.session.add(client)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'client': {
            'id': client.id,
            'nome': client.nome,
            'email': client.email,
            'telefone': client.telefone,
            'empresa': client.empresa,
            'endereco': client.endereco
        }
    }), 201


@api_v1.route('/clients/<int:client_id>', methods=['PUT'])
@require_system_api_key(required_scopes=['clients:write'])
def update_client(client_id):
    """Atualiza um cliente"""
    client = Client.query.get(client_id)
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    if 'nome' in data and data['nome']:
        client.nome = data['nome']
    if 'email' in data:
        client.email = data.get('email')
    if 'telefone' in data:
        client.telefone = data.get('telefone')
    if 'empresa' in data:
        client.empresa = data.get('empresa')
    if 'endereco' in data:
        client.endereco = data.get('endereco')
    if 'observacoes' in data:
        client.observacoes = data.get('observacoes')
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'client': {
            'id': client.id,
            'nome': client.nome,
            'email': client.email,
            'telefone': client.telefone,
            'empresa': client.empresa,
            'endereco': client.endereco
        }
    })


@api_v1.route('/clients/<int:client_id>', methods=['DELETE'])
@require_system_api_key(required_scopes=['clients:write'])
def delete_client(client_id):
    """Deleta um cliente"""
    client = Client.query.get(client_id)
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    if client.projects:
        return api_error('client_has_projects', 'Cliente possui projetos vinculados. Remova os projetos primeiro.', 400)
    
    db.session.delete(client)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cliente deletado com sucesso'
    })


# ============================================================================
# CRM API ENDPOINTS (Organized under /crm/ prefix)
# ============================================================================

@api_v1.route('/crm/clients', methods=['GET'])
@require_system_api_key(required_scopes=['clients:read'])
def crm_list_clients():
    """Lista todos os clientes (CRM)"""
    clients = Client.query.order_by(Client.nome).all()
    
    return jsonify({
        'success': True,
        'clients': [{
            'id': c.id,
            'nome': c.nome,
            'email': c.email,
            'telefone': c.telefone,
            'empresa': c.empresa,
            'endereco': c.endereco,
            'observacoes': c.observacoes,
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'projects_count': len(c.projects) if c.projects else 0
        } for c in clients],
        'total': len(clients)
    })


@api_v1.route('/crm/clients/<int:client_id>', methods=['GET'])
@require_system_api_key(required_scopes=['clients:read'])
def crm_get_client(client_id):
    """Retorna detalhes de um cliente (CRM)"""
    client = Client.query.get(client_id)
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    return jsonify({
        'success': True,
        'client': {
            'id': client.id,
            'nome': client.nome,
            'email': client.email,
            'telefone': client.telefone,
            'empresa': client.empresa,
            'endereco': client.endereco,
            'observacoes': client.observacoes,
            'created_at': client.created_at.isoformat() if client.created_at else None,
            'projects': [{
                'id': p.id,
                'nome': p.nome,
                'status': p.status
            } for p in client.projects] if client.projects else []
        }
    })


@api_v1.route('/crm/clients', methods=['POST'])
@require_system_api_key(required_scopes=['clients:write'])
def crm_create_client():
    """Cria um novo cliente (CRM)"""
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    if not data.get('nome'):
        return api_error('missing_field', 'Campo obrigatório: nome', 400)
    
    system_api_key = g.get('system_api_key')
    creator_id = system_api_key.user_id if system_api_key else 1
    
    client = Client(
        nome=data['nome'],
        email=data.get('email'),
        telefone=data.get('telefone'),
        empresa=data.get('empresa'),
        endereco=data.get('endereco'),
        observacoes=data.get('observacoes'),
        creator_id=creator_id
    )
    
    db.session.add(client)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'client': {
            'id': client.id,
            'nome': client.nome,
            'email': client.email,
            'telefone': client.telefone,
            'empresa': client.empresa,
            'endereco': client.endereco
        }
    }), 201


@api_v1.route('/crm/clients/<int:client_id>', methods=['PUT'])
@require_system_api_key(required_scopes=['clients:write'])
def crm_update_client(client_id):
    """Atualiza um cliente (CRM)"""
    client = Client.query.get(client_id)
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    if 'nome' in data and data['nome']:
        client.nome = data['nome']
    if 'email' in data:
        client.email = data.get('email')
    if 'telefone' in data:
        client.telefone = data.get('telefone')
    if 'empresa' in data:
        client.empresa = data.get('empresa')
    if 'endereco' in data:
        client.endereco = data.get('endereco')
    if 'observacoes' in data:
        client.observacoes = data.get('observacoes')
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'client': {
            'id': client.id,
            'nome': client.nome,
            'email': client.email,
            'telefone': client.telefone,
            'empresa': client.empresa,
            'endereco': client.endereco
        }
    })


@api_v1.route('/crm/clients/<int:client_id>', methods=['DELETE'])
@require_system_api_key(required_scopes=['clients:write'])
def crm_delete_client(client_id):
    """Deleta um cliente (CRM)"""
    client = Client.query.get(client_id)
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    if client.projects:
        return api_error('client_has_projects', 'Cliente possui projetos vinculados. Remova os projetos primeiro.', 400)
    
    db.session.delete(client)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cliente deletado com sucesso'
    })


# ============================================================================
# PROJECT SYSTEM API ENDPOINTS
# ============================================================================

@api_v1.route('/projects', methods=['GET'])
@require_system_api_key(required_scopes=['projects:read'])
def list_projects():
    """Lista todos os projetos"""
    status = request.args.get('status')
    client_id = request.args.get('client_id', type=int)
    
    query = Project.query
    
    if status:
        query = query.filter_by(status=status)
    if client_id:
        query = query.filter_by(client_id=client_id)
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'projects': [{
            'id': p.id,
            'nome': p.nome,
            'status': p.status,
            'progress_percent': p.progress_percent,
            'prazo': p.prazo.isoformat() if p.prazo else None,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'client': {
                'id': p.client.id,
                'nome': p.client.nome
            } if p.client else None,
            'responsible': {
                'id': p.responsible.id,
                'nome': p.responsible.nome
            } if p.responsible else None,
            'tasks_count': len(p.tasks) if p.tasks else 0
        } for p in projects],
        'total': len(projects)
    })


@api_v1.route('/projects/<int:project_id>', methods=['GET'])
@require_system_api_key(required_scopes=['projects:read'])
def get_project_detail(project_id):
    """Retorna detalhes de um projeto"""
    project = Project.query.get(project_id)
    if not project:
        return api_error('project_not_found', 'Projeto não encontrado', 404)
    
    return jsonify({
        'success': True,
        'project': {
            'id': project.id,
            'nome': project.nome,
            'status': project.status,
            'progress_percent': project.progress_percent,
            'prazo': project.prazo.isoformat() if project.prazo else None,
            'created_at': project.created_at.isoformat() if project.created_at else None,
            'descricao_resumida': project.descricao_resumida,
            'objetivos': project.objetivos,
            'escopo': project.escopo,
            'restricoes': project.restricoes,
            'client': {
                'id': project.client.id,
                'nome': project.client.nome
            } if project.client else None,
            'responsible': {
                'id': project.responsible.id,
                'nome': project.responsible.nome
            } if project.responsible else None,
            'team_members': [{
                'id': m.id,
                'nome': m.nome
            } for m in project.team_members] if project.team_members else [],
            'tasks': [{
                'id': t.id,
                'titulo': t.titulo,
                'status': t.status
            } for t in project.tasks] if project.tasks else []
        }
    })


@api_v1.route('/projects', methods=['POST'])
@require_system_api_key(required_scopes=['projects:write'])
def create_project_system():
    """Cria um novo projeto"""
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    if not data.get('nome'):
        return api_error('missing_field', 'Campo obrigatório: nome', 400)
    if not data.get('client_id'):
        return api_error('missing_field', 'Campo obrigatório: client_id', 400)
    
    client = Client.query.get(data['client_id'])
    if not client:
        return api_error('client_not_found', 'Cliente não encontrado', 404)
    
    project = Project(
        nome=data['nome'],
        client_id=data['client_id'],
        responsible_id=data.get('responsible_id'),
        status=data.get('status', 'em_andamento'),
        descricao_resumida=data.get('descricao_resumida'),
        objetivos=data.get('objetivos'),
        escopo=data.get('escopo'),
        restricoes=data.get('restricoes')
    )
    
    if data.get('prazo'):
        try:
            project.prazo = datetime.fromisoformat(data['prazo']).date()
        except:
            pass
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'project': {
            'id': project.id,
            'nome': project.nome,
            'status': project.status
        }
    }), 201


@api_v1.route('/projects/<int:project_id>', methods=['PUT'])
@require_system_api_key(required_scopes=['projects:write'])
def update_project_system(project_id):
    """Atualiza um projeto"""
    project = Project.query.get(project_id)
    if not project:
        return api_error('project_not_found', 'Projeto não encontrado', 404)
    
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    updatable_fields = ['nome', 'status', 'descricao_resumida', 'objetivos', 'escopo', 'restricoes', 'responsible_id', 'client_id']
    
    for field in updatable_fields:
        if field in data:
            setattr(project, field, data[field])
    
    if 'prazo' in data:
        if data['prazo']:
            try:
                project.prazo = datetime.fromisoformat(data['prazo']).date()
            except:
                pass
        else:
            project.prazo = None
    
    if 'progress_percent' in data:
        project.progress_percent = max(0, min(100, int(data['progress_percent'])))
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'project': {
            'id': project.id,
            'nome': project.nome,
            'status': project.status,
            'progress_percent': project.progress_percent
        }
    })


@api_v1.route('/projects/<int:project_id>', methods=['DELETE'])
@require_system_api_key(required_scopes=['projects:write'])
def delete_project_system(project_id):
    """Deleta um projeto"""
    project = Project.query.get(project_id)
    if not project:
        return api_error('project_not_found', 'Projeto não encontrado', 404)
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Projeto deletado com sucesso'
    })


@api_v1.route('/system/tasks', methods=['GET'])
@require_system_api_key(required_scopes=['tasks:read'])
def list_all_tasks():
    """Lista todas as tarefas do sistema (sem filtro de projeto)"""
    status = request.args.get('status')
    project_id = request.args.get('project_id', type=int)
    assigned_user_id = request.args.get('assigned_user_id', type=int)
    
    query = Task.query
    
    if status:
        query = query.filter_by(status=status)
    if project_id:
        query = query.filter_by(project_id=project_id)
    if assigned_user_id:
        query = query.filter_by(assigned_user_id=assigned_user_id)
    
    tasks = query.order_by(Task.created_at.desc()).limit(100).all()
    
    def build_task_response(t):
        task_data = {
            'id': t.id,
            'titulo': t.titulo,
            'descricao': t.descricao,
            'status': t.status,
            'ordem': t.ordem,
            'disparada': t.disparada,
            'data_conclusao': t.data_conclusao.isoformat() if t.data_conclusao else None,
            'created_at': t.created_at.isoformat() if t.created_at else None,
            'completed_at': t.completed_at.isoformat() if t.completed_at else None,
            'project': {
                'id': t.project.id,
                'nome': t.project.nome
            } if t.project else None,
            'assigned_user': {
                'id': t.assigned_user.id,
                'nome': t.assigned_user.nome
            } if t.assigned_user else None
        }
        
        if t.status in ('pendente', 'em_andamento'):
            task_data['todos'] = [{
                'id': todo.id,
                'texto': todo.texto,
                'comentario': todo.comentario,
                'completed': todo.completed,
                'due_date': todo.due_date.isoformat() if todo.due_date else None,
                'created_at': todo.created_at.isoformat() if todo.created_at else None,
                'completed_at': todo.completed_at.isoformat() if todo.completed_at else None
            } for todo in t.todos]
        
        return task_data
    
    return jsonify({
        'success': True,
        'tasks': [build_task_response(t) for t in tasks],
        'total': len(tasks)
    })


@api_v1.route('/system/tasks', methods=['POST'])
@require_system_api_key(required_scopes=['tasks:write'])
def create_task_system():
    """Cria uma tarefa em qualquer projeto"""
    data = request.get_json()
    if not data:
        return api_error('invalid_json', 'JSON inválido ou não fornecido', 400)
    
    if not data.get('titulo'):
        return api_error('missing_field', 'Campo obrigatório: titulo', 400)
    if not data.get('project_id'):
        return api_error('missing_field', 'Campo obrigatório: project_id', 400)
    
    project = Project.query.get(data['project_id'])
    if not project:
        return api_error('project_not_found', 'Projeto não encontrado', 404)
    
    task = Task(
        titulo=data['titulo'],
        descricao=data.get('descricao', ''),
        status=data.get('status', 'pendente'),
        project_id=data['project_id']
    )
    
    if data.get('assigned_user_id'):
        user = User.query.get(data['assigned_user_id'])
        if user:
            task.assigned_user_id = user.id
    
    if data.get('data_conclusao'):
        try:
            task.data_conclusao = datetime.fromisoformat(data['data_conclusao']).date()
        except:
            pass
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': {
            'id': task.id,
            'titulo': task.titulo,
            'status': task.status,
            'project_id': task.project_id
        }
    }), 201


@api_v1.route('/users', methods=['GET'])
@require_system_api_key(required_scopes=['users:read'])
def list_users():
    """Lista todos os usuários do sistema"""
    users = User.query.order_by(User.nome).all()
    
    return jsonify({
        'success': True,
        'users': [{
            'id': u.id,
            'nome': u.nome,
            'sobrenome': u.sobrenome,
            'email': u.email,
            'is_admin': u.is_admin,
            'created_at': u.created_at.isoformat() if hasattr(u, 'created_at') and u.created_at else None
        } for u in users],
        'total': len(users)
    })


@api_v1.route('/users/<int:user_id>', methods=['GET'])
@require_system_api_key(required_scopes=['users:read'])
def get_user(user_id):
    """Retorna detalhes de um usuário"""
    user = User.query.get(user_id)
    if not user:
        return api_error('user_not_found', 'Usuário não encontrado', 404)
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'nome': user.nome,
            'sobrenome': user.sobrenome,
            'email': user.email,
            'is_admin': user.is_admin,
            'tasks_count': Task.query.filter_by(assigned_user_id=user.id).count()
        }
    })
