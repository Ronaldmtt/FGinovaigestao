from extensions import db
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
    empresa = db.Column(db.String(200))
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
    progress_percent = db.Column(db.Integer, default=0)  # Progresso do projeto em percentagem (0-100)
    prazo = db.Column(db.Date)  # Data de prazo do projeto (mantido por compatibilidade ou redundância)
    data_inicio = db.Column(db.Date)  # Data de início do projeto
    data_fim = db.Column(db.Date)  # Data de previsão de término (entrega)
    
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
    
    # Controle de visibilidade no Kanban
    show_in_kanban = db.Column(db.Boolean, default=True, nullable=False)
    
    # Indicadores de Conteúdo
    has_github = db.Column(db.Boolean, default=False, nullable=False)
    has_drive = db.Column(db.Boolean, default=False, nullable=False)
    has_env = db.Column(db.Boolean, default=False, nullable=False)
    has_backup_db = db.Column(db.Boolean, default=False, nullable=False)
    
    # Integração RPA
    rpa_identifier = db.Column(db.String(100), nullable=True)

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


class ContatoFile(db.Model):
    __tablename__ = 'contato_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    storage_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'), nullable=False)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    contato = db.relationship('Contato', backref=db.backref('arquivos', lazy=True, cascade='all, delete-orphan'))
    uploaded_by = db.relationship('User', backref='uploaded_contato_files')
    
    def __repr__(self):
        return f'<ContatoFile {self.original_name}>'
    
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
    def is_pdf(self):
        return self.mime_type == 'application/pdf'


class ProjectApiKey(db.Model):
    """Chave de API por projeto/usuário para acesso à API v1"""
    __tablename__ = 'project_api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    prefix = db.Column(db.String(12), unique=True, nullable=False, index=True)
    key_hash = db.Column(db.String(256), nullable=False)
    scopes_json = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    revoked_at = db.Column(db.DateTime)
    
    project = db.relationship('Project', backref=db.backref('api_keys', lazy=True, cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('project_api_keys', lazy=True))
    
    def __repr__(self):
        return f'<ProjectApiKey {self.name} ({self.prefix}...)>'
    
    @property
    def scopes(self):
        import json
        try:
            return json.loads(self.scopes_json) if self.scopes_json else []
        except:
            return []
    
    @scopes.setter
    def scopes(self, value):
        import json
        self.scopes_json = json.dumps(value) if value else '[]'
    
    def has_scope(self, required_scope):
        return required_scope in self.scopes
    
    def is_active(self):
        from datetime import datetime
        if self.revoked_at:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
    
    @property
    def masked_prefix(self):
        return f"{self.prefix}..."
    
    def to_dict(self, include_sensitive=False):
        from datetime import datetime
        is_expired = self.expires_at and datetime.utcnow() > self.expires_at
        data = {
            'id': self.id,
            'name': self.name,
            'prefix': self.prefix,
            'scopes': self.scopes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active(),
            'is_revoked': self.revoked_at is not None,
            'is_expired': bool(is_expired)
        }
        return data


class Lead(db.Model):
    """Lead/Prospecto do CRM"""
    __tablename__ = 'lead'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    empresa = db.Column(db.String(200))
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(50))
    cargo = db.Column(db.String(100))
    origem = db.Column(db.String(100))
    valor_estimado = db.Column(db.Float)
    etapa = db.Column(db.String(50), nullable=False, default='Novo')
    convertido = db.Column(db.Boolean, default=False, nullable=False)
    perdido = db.Column(db.Boolean, default=False, nullable=False)
    motivo_perda = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    responsavel_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    converted_to_client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    
    responsavel = db.relationship('User', backref=db.backref('leads_responsavel', lazy=True))
    converted_to_client = db.relationship('Client', backref=db.backref('converted_from_leads', lazy=True))
    
    def __repr__(self):
        return f'<Lead {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'empresa': self.empresa,
            'email': self.email,
            'telefone': self.telefone,
            'cargo': self.cargo,
            'origem': self.origem,
            'valor_estimado': self.valor_estimado,
            'etapa': self.etapa,
            'convertido': self.convertido,
            'perdido': self.perdido,
            'motivo_perda': self.motivo_perda,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'responsavel_id': self.responsavel_id,
            'responsavel_nome': self.responsavel.full_name if self.responsavel else None,
            'converted_to_client_id': self.converted_to_client_id
        }


class SystemApiKey(db.Model):
    """Chave de API geral do sistema (não vinculada a projeto específico)"""
    __tablename__ = 'system_api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    prefix = db.Column(db.String(12), unique=True, nullable=False, index=True)
    key_hash = db.Column(db.String(256), nullable=False)
    scopes_json = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    revoked_at = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('system_api_keys', lazy=True))
    
    def __repr__(self):
        return f'<SystemApiKey {self.name} ({self.prefix}...)>'
    
    @property
    def scopes(self):
        import json
        try:
            return json.loads(self.scopes_json) if self.scopes_json else []
        except:
            return []
    
    @scopes.setter
    def scopes(self, value):
        import json
        self.scopes_json = json.dumps(value) if value else '[]'
    
    def has_scope(self, required_scope):
        return required_scope in self.scopes
    
    def is_active(self):
        from datetime import datetime
        if self.revoked_at:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
    
    @property
    def masked_prefix(self):
        return f"{self.prefix}..."
    
    def to_dict(self, include_sensitive=False):
        from datetime import datetime
        is_expired = self.expires_at and datetime.utcnow() > self.expires_at
        data = {
            'id': self.id,
            'name': self.name,
            'prefix': self.prefix,
            'scopes': self.scopes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active(),
            'is_revoked': self.revoked_at is not None,
            'is_expired': bool(is_expired)
        }
        return data
