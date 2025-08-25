from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from wtforms.widgets import TextArea
from models import User, Client, Project

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    sobrenome = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Administrador')
    
    def validate_email(self, email):
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
    team_members = SelectField('Membros da Equipe', coerce=int, choices=[])
    transcricao = TextAreaField('Transcrição', widget=TextArea(), render_kw={"rows": 10})
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, c.nome) for c in Client.query.all()]
        self.responsible_id.choices = [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).all()]
        self.team_members.choices = [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).all()]

class TaskForm(FlaskForm):
    titulo = StringField('Título da Tarefa', validators=[DataRequired(), Length(min=2, max=200)])
    descricao = TextAreaField('Descrição')
    project_id = SelectField('Projeto', coerce=int, validators=[DataRequired()])
    assigned_user_id = SelectField('Usuário Responsável', coerce=int)
    data_conclusao = DateField('Data de Conclusão')
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.project_id.choices = [(p.id, f"{p.client.nome} - {p.nome}") for p in Project.query.all()]
        self.assigned_user_id.choices = [('', 'Selecione um usuário')] + [(u.id, u.full_name) for u in User.query.filter_by(is_admin=False).all()]

class TranscriptionTaskForm(FlaskForm):
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Projeto', coerce=int, validators=[DataRequired()])
    transcricao = TextAreaField('Transcrição', validators=[DataRequired()], widget=TextArea(), render_kw={"rows": 10})
    
    def __init__(self, *args, **kwargs):
        super(TranscriptionTaskForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, c.nome) for c in Client.query.all()]
        self.project_id.choices = [('', 'Selecione um projeto')] + [(p.id, p.nome) for p in Project.query.all()]
