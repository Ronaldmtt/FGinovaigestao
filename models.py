from app import db
from flask_login import UserMixin
from datetime import datetime

# Tabela de associação para usuários em projetos (equipe)
project_users = db.Table('project_users',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    reset_token = db.Column(db.String(100))
    reset_token_expires = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Permissões de acesso às abas
    acesso_clientes = db.Column(db.Boolean, default=True, nullable=False)
    acesso_projetos = db.Column(db.Boolean, default=True, nullable=False)
    acesso_tarefas = db.Column(db.Boolean, default=True, nullable=False)
    acesso_kanban = db.Column(db.Boolean, default=True, nullable=False)
    acesso_crm = db.Column(db.Boolean, default=True, nullable=False)
    
    # Notificações por email
    receber_notificacoes = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relacionamentos
    created_clients = db.relationship('Client', backref='creator', lazy=True)
    responsible_projects = db.relationship('Project', backref='responsible', lazy=True, foreign_keys='Project.responsible_id')
    assigned_tasks = db.relationship('Task', backref='assigned_user', lazy=True, foreign_keys='Task.assigned_user_id')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @property
    def full_name(self):
        return f"{self.nome} {self.sobrenome}"

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    public_code = db.Column(db.String(32), unique=True)  # Código único para acesso público
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamentos
    projects = db.relationship('Project', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.nome}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    transcricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='em_andamento', nullable=False)  # em_andamento, pausado, cancelado, concluido
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress_percent = db.Column(db.Integer, default=0)  # Progresso do projeto em percentagem (0-100)
    prazo = db.Column(db.Date)  # Data de prazo do projeto
    
    # Foreign keys
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Campos preenchidos pela IA
    contexto_justificativa = db.Column(db.Text)
    descricao_resumida = db.Column(db.Text)
    problema_oportunidade = db.Column(db.Text)
    objetivos = db.Column(db.Text)
    alinhamento_estrategico = db.Column(db.Text)
    escopo_projeto = db.Column(db.Text)
    fora_escopo = db.Column(db.Text)
    premissas = db.Column(db.Text)
    restricoes = db.Column(db.Text)
    
    # Relacionamentos many-to-many com usuários (equipe)
    team_members = db.relationship('User', secondary=project_users, backref=db.backref('team_projects', lazy='dynamic'))
    tasks = db.relationship('Task', backref='project', lazy=True)
    
    def __repr__(self):
        return f'<Project {self.nome}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente', nullable=False)  # pendente, em_andamento, concluida
    data_conclusao = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    disparada = db.Column(db.Boolean, default=False, nullable=False)
    disparada_at = db.Column(db.DateTime)
    ordem = db.Column(db.Integer, default=0)  # Ordem dentro da coluna do Kanban
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relacionamentos
    todos = db.relationship('TodoItem', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.titulo}>'

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(300), nullable=False)
    comentario = db.Column(db.Text)  # Comentário/observação do to-do
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    due_date = db.Column(db.Date)  # Data de vencimento do to-do
    
    # Foreign key
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    
    def __repr__(self):
        return f'<TodoItem {self.texto}>'

class Contato(db.Model):
    __tablename__ = 'contatos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_empresa = db.Column(db.String(200), nullable=False)
    nome_contato = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    estagio = db.Column(db.String(100), nullable=False, default='Captação')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comentarios = db.relationship('Comentario', backref='contato', lazy=True, cascade='all, delete-orphan', order_by='Comentario.data_criacao.desc()')
    
    def __repr__(self):
        return f'<Contato {self.nome_empresa} - {self.nome_contato}>'


class Comentario(db.Model):
    __tablename__ = 'comentarios'
    
    id = db.Column(db.Integer, primary_key=True)
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comentario {self.id} - Contato {self.contato_id}>'

class CrmStage(db.Model):
    __tablename__ = 'crm_stages'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    ordem = db.Column(db.Integer, nullable=False)
    is_fixed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CrmStage {self.nome}>'


class FileCategory(db.Model):
    __tablename__ = 'file_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    icone = db.Column(db.String(50), default='fa-folder')
    cor = db.Column(db.String(20), default='#6b7280')
    ordem = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    files = db.relationship('ProjectFile', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<FileCategory {self.nome}>'


class ProjectFile(db.Model):
    __tablename__ = 'project_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    storage_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('file_categories.id'))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    project = db.relationship('Project', backref=db.backref('files', lazy=True, cascade='all, delete-orphan'))
    uploaded_by = db.relationship('User', backref='uploaded_files')
    
    def __repr__(self):
        return f'<ProjectFile {self.original_name}>'
    
    @property
    def file_size_formatted(self):
        if not self.file_size:
            return '0 B'
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} TB'
    
    @property
    def is_image(self):
        return self.mime_type and self.mime_type.startswith('image/')
    
    @property
    def is_video(self):
        return self.mime_type and self.mime_type.startswith('video/')
    
    @property
    def is_pdf(self):
        return self.mime_type == 'application/pdf'


class ProjectApiCredential(db.Model):
    __tablename__ = 'project_api_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    provedor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    api_key_masked = db.Column(db.String(50))
    api_key_encrypted = db.Column(db.Text)
    ambiente = db.Column(db.String(20), default='development')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    project = db.relationship('Project', backref=db.backref('api_credentials', lazy=True, cascade='all, delete-orphan'))
    created_by = db.relationship('User', backref='created_credentials')
    
    def __repr__(self):
        return f'<ProjectApiCredential {self.nome}>'


class ProjectApiEndpoint(db.Model):
    __tablename__ = 'project_api_endpoints'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    metodo = db.Column(db.String(10), default='GET')
    descricao = db.Column(db.Text)
    headers = db.Column(db.Text)
    body_exemplo = db.Column(db.Text)
    documentacao_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    credential_id = db.Column(db.Integer, db.ForeignKey('project_api_credentials.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    project = db.relationship('Project', backref=db.backref('api_endpoints', lazy=True, cascade='all, delete-orphan'))
    credential = db.relationship('ProjectApiCredential', backref='endpoints')
    created_by = db.relationship('User', backref='created_endpoints')
    
    def __repr__(self):
        return f'<ProjectApiEndpoint {self.nome}>'
