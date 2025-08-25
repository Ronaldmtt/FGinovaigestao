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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Foreign key
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    
    def __repr__(self):
        return f'<TodoItem {self.texto}>'
