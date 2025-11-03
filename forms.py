from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Optional
from wtforms.widgets import TextArea
from models import User, Client, Project
from sqlalchemy import func

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    sobrenome = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Administrador')
    
    acesso_clientes = BooleanField('Acesso a Clientes', default=True)
    acesso_projetos = BooleanField('Acesso a Projetos', default=True)
    acesso_tarefas = BooleanField('Acesso a Tarefas', default=True)
    acesso_kanban = BooleanField('Acesso ao Kanban', default=True)
    acesso_crm = BooleanField('Acesso ao CRM', default=True)
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está em uso.')

class EditUserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    sobrenome = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Nova Senha', validators=[Optional(), Length(min=6)])  # Senha opcional para edição
    is_admin = BooleanField('Administrador')
    
    acesso_clientes = BooleanField('Acesso a Clientes', default=True)
    acesso_projetos = BooleanField('Acesso a Projetos', default=True)
    acesso_tarefas = BooleanField('Acesso a Tarefas', default=True)
    acesso_kanban = BooleanField('Acesso ao Kanban', default=True)
    acesso_crm = BooleanField('Acesso ao CRM', default=True)
    receber_notificacoes = BooleanField('Receber Notificações por Email', default=True)
    
    def __init__(self, original_email, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este email já está em uso.')

class ClientForm(FlaskForm):
    nome = StringField('Nome do Cliente', validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('Email')
    telefone = StringField('Telefone')
    endereco = TextAreaField('Endereço')

class ProjectForm(FlaskForm):
    nome = StringField('Nome do Projeto', validators=[DataRequired(), Length(min=2, max=200)])
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    responsible_id = SelectField('Usuário Responsável', coerce=int, validators=[DataRequired()])
    team_members = SelectMultipleField('Membros da Equipe', coerce=int, choices=[])
    status = SelectField('Status', choices=[
        ('em_andamento', 'Em Andamento'),
        ('pausado', 'Pausado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído')
    ], default='em_andamento', validators=[DataRequired()])
    transcricao = TextAreaField('Transcrição', widget=TextArea(), render_kw={"rows": 10})
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, c.nome) for c in Client.query.order_by(Client.nome).all()]
        self.responsible_id.choices = [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()]
        self.team_members.choices = [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()]

class TaskForm(FlaskForm):
    titulo = StringField('Título da Tarefa', validators=[DataRequired(), Length(min=2, max=200)])
    descricao = TextAreaField('Descrição')
    project_id = SelectField('Projeto', coerce=int, validators=[DataRequired()])
    assigned_user_id = SelectField('Usuário Responsável', coerce=int)
    data_conclusao = DateField('Data de Conclusão')
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.project_id.choices = [(p.id, f"{p.client.nome} - {p.nome}") for p in Project.query.join(Client).order_by(Client.nome, Project.nome).all()]
        self.assigned_user_id.choices = [(0, 'Selecione um usuário')] + [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()]

class TranscriptionTaskForm(FlaskForm):
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Projeto', coerce=int, validators=[DataRequired()])
    transcricao = TextAreaField('Transcrição', validators=[DataRequired()], widget=TextArea(), render_kw={"rows": 10})
    
    def __init__(self, *args, **kwargs):
        super(TranscriptionTaskForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, c.nome) for c in Client.query.order_by(Client.nome).all()]
        self.project_id.choices = [(0, 'Selecione um projeto')] + [(p.id, p.nome) for p in Project.query.order_by(Project.nome).all()]

class ManualProjectForm(FlaskForm):
    nome = StringField('Nome do Projeto', validators=[DataRequired(), Length(min=2, max=200)])
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    responsible_id = SelectField('Usuário Responsável', coerce=int, validators=[DataRequired()])
    team_members = SelectMultipleField('Membros da Equipe', coerce=int, choices=[])
    status = SelectField('Status', choices=[
        ('em_andamento', 'Em Andamento'),
        ('pausado', 'Pausado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído')
    ], default='em_andamento', validators=[DataRequired()])
    
    # Campos detalhados do projeto
    descricao_resumida = TextAreaField('Descrição Resumida', render_kw={"rows": 3})
    problema_oportunidade = TextAreaField('Problema/Oportunidade', render_kw={"rows": 3})
    objetivos = TextAreaField('Objetivos', render_kw={"rows": 3})
    alinhamento_estrategico = TextAreaField('Alinhamento Estratégico', render_kw={"rows": 3})
    escopo_projeto = TextAreaField('Escopo do Projeto', render_kw={"rows": 4})
    fora_escopo = TextAreaField('Fora do Escopo', render_kw={"rows": 3})
    premissas = TextAreaField('Premissas', render_kw={"rows": 3})
    restricoes = TextAreaField('Restrições', render_kw={"rows": 3})
    
    def __init__(self, *args, **kwargs):
        super(ManualProjectForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, c.nome) for c in Client.query.order_by(Client.nome).all()]
        self.responsible_id.choices = [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()]
        self.team_members.choices = [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()]

class ManualTaskForm(FlaskForm):
    titulo = StringField('Título da Tarefa', validators=[DataRequired(), Length(min=2, max=200)])
    descricao = TextAreaField('Descrição Detalhada', validators=[DataRequired()], render_kw={"rows": 4})
    project_id = SelectField('Projeto', coerce=int, validators=[DataRequired()])
    assigned_user_id = SelectField('Usuário Responsável', coerce=int)
    data_conclusao = DateField('Data de Conclusão')
    status = SelectField('Status', choices=[
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída')
    ], default='pendente', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(ManualTaskForm, self).__init__(*args, **kwargs)
        self.project_id.choices = [(p.id, f"{p.client.nome} - {p.nome}") for p in Project.query.join(Client).order_by(Client.nome, Project.nome).all()]
        self.assigned_user_id.choices = [('', 'Selecione um usuário')] + [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).order_by(func.lower(User.nome), func.lower(User.sobrenome)).all()]

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Por favor, digite um email válido.")])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(),
        EqualTo('password', message="As senhas devem ser iguais.")
    ])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(),
        EqualTo('new_password', message="As senhas devem ser iguais.")
    ])

class ImportDataForm(FlaskForm):
    data_file = StringField('Arquivo JSON', validators=[DataRequired()])
