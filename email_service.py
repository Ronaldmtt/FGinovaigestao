from flask_mail import Message
from extensions import mail
from app import app
from flask import render_template
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def enviar_email_nova_tarefa(usuario, tarefa, projeto):
    """
    Envia email quando uma nova tarefa é atribuída ao usuário
    """
    if not usuario or not usuario.email or not usuario.receber_notificacoes:
        return False
    
    try:
        msg = Message(
            subject=f'Nova Tarefa Atribuída: {tarefa.titulo}',
            recipients=[usuario.email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.html = render_template('email/nova_tarefa.html',
                                   usuario=usuario,
                                   tarefa=tarefa,
                                   projeto=projeto)
        
        msg.body = f"""
Olá {usuario.nome},

Você recebeu uma nova tarefa!

Tarefa: {tarefa.titulo}
Projeto: {projeto.nome}
Descrição: {tarefa.descricao if tarefa.descricao else 'Sem descrição'}
Data de Conclusão: {tarefa.data_conclusao.strftime('%d/%m/%Y') if tarefa.data_conclusao else 'Não definida'}

Acesse o sistema para mais detalhes.

---
Este é um email automático. Você pode desativar notificações nas configurações do seu perfil.
        """
        
        with app.app_context():
            mail.send(msg)
        
        logger.info(f"Email enviado para {usuario.email} - Nova tarefa: {tarefa.titulo}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email para {usuario.email}: {str(e)}")
        return False


def enviar_email_mudanca_status(usuario, tarefa, projeto, status_antigo, status_novo):
    """
    Envia email quando o status de uma tarefa muda
    """
    if not usuario or not usuario.email or not usuario.receber_notificacoes:
        return False
    
    status_dict = {
        'pendente': 'Pendente',
        'em_andamento': 'Em Andamento',
        'concluida': 'Concluída'
    }
    
    try:
        msg = Message(
            subject=f'Status Alterado: {tarefa.titulo}',
            recipients=[usuario.email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.html = render_template('email/mudanca_status.html',
                                   usuario=usuario,
                                   tarefa=tarefa,
                                   projeto=projeto,
                                   status_antigo=status_dict.get(status_antigo, status_antigo),
                                   status_novo=status_dict.get(status_novo, status_novo))
        
        msg.body = f"""
Olá {usuario.nome},

O status de uma tarefa foi alterado!

Tarefa: {tarefa.titulo}
Projeto: {projeto.nome}
Status Anterior: {status_dict.get(status_antigo, status_antigo)}
Novo Status: {status_dict.get(status_novo, status_novo)}

Acesse o sistema para mais detalhes.

---
Este é um email automático. Você pode desativar notificações nas configurações do seu perfil.
        """
        
        with app.app_context():
            mail.send(msg)
        
        logger.info(f"Email enviado para {usuario.email} - Mudança status: {tarefa.titulo}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email para {usuario.email}: {str(e)}")
        return False


def enviar_email_alteracao_data(usuario, tarefa, projeto, data_antiga, data_nova):
    """
    Envia email quando a data de conclusão de uma tarefa é alterada
    """
    if not usuario or not usuario.email or not usuario.receber_notificacoes:
        return False
    
    try:
        msg = Message(
            subject=f'Data Alterada: {tarefa.titulo}',
            recipients=[usuario.email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        
        data_antiga_str = data_antiga.strftime('%d/%m/%Y') if data_antiga else 'Não definida'
        data_nova_str = data_nova.strftime('%d/%m/%Y') if data_nova else 'Não definida'
        
        msg.html = render_template('email/alteracao_data.html',
                                   usuario=usuario,
                                   tarefa=tarefa,
                                   projeto=projeto,
                                   data_antiga=data_antiga_str,
                                   data_nova=data_nova_str)
        
        msg.body = f"""
Olá {usuario.nome},

A data de conclusão de uma tarefa foi alterada!

Tarefa: {tarefa.titulo}
Projeto: {projeto.nome}
Data Anterior: {data_antiga_str}
Nova Data: {data_nova_str}

Acesse o sistema para mais detalhes.

---
Este é um email automático. Você pode desativar notificações nas configurações do seu perfil.
        """
        
        with app.app_context():
            mail.send(msg)
        
        logger.info(f"Email enviado para {usuario.email} - Alteração data: {tarefa.titulo}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email para {usuario.email}: {str(e)}")
        return False


def enviar_email_tarefa_editada(usuario, tarefa, projeto):
    """
    Envia email quando uma tarefa é editada (título ou descrição)
    """
    if not usuario or not usuario.email or not usuario.receber_notificacoes:
        return False
    
    try:
        msg = Message(
            subject=f'Tarefa Editada: {tarefa.titulo}',
            recipients=[usuario.email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.html = render_template('email/tarefa_editada.html',
                                   usuario=usuario,
                                   tarefa=tarefa,
                                   projeto=projeto)
        
        msg.body = f"""
Olá {usuario.nome},

Uma tarefa atribuída a você foi editada!

Tarefa: {tarefa.titulo}
Projeto: {projeto.nome}
Descrição: {tarefa.descricao if tarefa.descricao else 'Sem descrição'}
Data de Conclusão: {tarefa.data_conclusao.strftime('%d/%m/%Y') if tarefa.data_conclusao else 'Não definida'}

Acesse o sistema para mais detalhes.

---
Este é um email automático. Você pode desativar notificações nas configurações do seu perfil.
        """
        
        with app.app_context():
            mail.send(msg)
        
        logger.info(f"Email enviado para {usuario.email} - Tarefa editada: {tarefa.titulo}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email para {usuario.email}: {str(e)}")
        return False


def enviar_email_resumo_tarefas(usuario, tarefas, filtro_info=""):
    """
    Envia email com resumo de tarefas organizadas por status
    """
    if not usuario or not usuario.email or not usuario.receber_notificacoes:
        return False
    
    try:
        # Organizar tarefas por status
        tarefas_pendentes = [t for t in tarefas if t.status == 'pendente']
        tarefas_em_andamento = [t for t in tarefas if t.status == 'em_andamento']
        tarefas_concluidas = [t for t in tarefas if t.status == 'concluida']
        
        msg = Message(
            subject=f'Resumo de Tarefas - {len(tarefas)} tarefas',
            recipients=[usuario.email],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.html = render_template('email/resumo_tarefas.html',
                                   usuario_nome=usuario.full_name,
                                   tarefas_pendentes=tarefas_pendentes,
                                   tarefas_em_andamento=tarefas_em_andamento,
                                   tarefas_concluidas=tarefas_concluidas,
                                   total_tarefas=len(tarefas),
                                   filtro_info=filtro_info)
        
        msg.body = f"""
Olá {usuario.nome},

Aqui está um resumo das suas tarefas{filtro_info}:

Total de tarefas: {len(tarefas)}
- Pendentes: {len(tarefas_pendentes)}
- Em Andamento: {len(tarefas_em_andamento)}
- Concluídas: {len(tarefas_concluidas)}

Acesse o sistema para visualizar os detalhes completos.

---
Este é um email automático. Você pode desativar notificações nas configurações do seu perfil.
        """
        
        with app.app_context():
            mail.send(msg)
        
        logger.info(f"Email de resumo enviado para {usuario.email} - {len(tarefas)} tarefas")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email de resumo para {usuario.email}: {str(e)}")
        return False
