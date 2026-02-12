"""
Email Service — SMTP (Gmail) para envio de emails do CRM 2.
Usa smtplib puro, sem dependência de Flask-Mail.
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "")

def _get_sender():
    """Always use MAIL_USERNAME as the From to avoid Gmail domain mismatch."""
    return f"GESTAO INOVA <{MAIL_USERNAME}>" if MAIL_USERNAME else MAIL_DEFAULT_SENDER


def is_email_configured():
    """Verifica se as credenciais SMTP estão preenchidas."""
    return bool(MAIL_USERNAME and MAIL_PASSWORD)

# Module-level variable to store the last SMTP error for diagnostics
_last_smtp_error = None


def send_email(to, subject, html_body, text_body=None, attachment_path=None):
    """
    Envia um email via SMTP.
    
    Args:
        to: Email do destinatário (string ou lista)
        subject: Assunto do email
        html_body: Corpo HTML do email
        text_body: Corpo texto puro (fallback)
        attachment_path: Caminho para arquivo anexo (ex: PDF)
    
    Returns:
        True se enviou com sucesso, False caso contrário.
    """
    if not is_email_configured():
        print(f"[email] SMTP não configurado, email não enviado para {to}")
        return False
    
    try:
        sender = _get_sender()
        print(f"[email] Preparando envio: de={sender}, para={to}, assunto={subject}")
        print(f"[email] SMTP config: server={MAIL_SERVER}, port={MAIL_PORT}, tls={MAIL_USE_TLS}, user={MAIL_USERNAME}")
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = sender
        
        if isinstance(to, list):
            msg["To"] = ", ".join(to)
            recipients = to
        else:
            msg["To"] = to
            recipients = [to]
        
        # Body (alternative part for text/html)
        body_part = MIMEMultipart("alternative")
        if text_body:
            body_part.attach(MIMEText(text_body, "plain", "utf-8"))
        body_part.attach(MIMEText(html_body, "html", "utf-8"))
        msg.attach(body_part)
        
        # Attachment
        if attachment_path:
            import os
            from email.mime.application import MIMEApplication
            if os.path.exists(attachment_path):
                with open(attachment_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)
        
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            if MAIL_USE_TLS:
                server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, recipients, msg.as_string())
        
        print(f"[email] Email enviado com sucesso para {to}: {subject}")
        return True
        
    except Exception as e:
        global _last_smtp_error
        _last_smtp_error = str(e)
        print(f"[email] Erro ao enviar email para {to}: {e}")
        import traceback
        traceback.print_exc()
        return False


def _base_template(content, title):
    """Template base HTML para emails."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f4f7; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 15px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 25px 30px; }}
        .header h1 {{ margin: 0; font-size: 22px; }}
        .header .logo {{ font-size: 14px; opacity: 0.9; margin-bottom: 8px; }}
        .body {{ padding: 30px; }}
        .info-box {{ background: #f8f9fa; border-left: 4px solid #6366f1; padding: 15px; border-radius: 0 8px 8px 0; margin: 15px 0; }}
        .info-box p {{ margin: 5px 0; }}
        .button {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 15px 0; }}
        .button-accept {{ background: linear-gradient(135deg, #22c55e, #16a34a); }}
        .button-reject {{ background: linear-gradient(135deg, #ef4444, #dc2626); }}
        .footer {{ padding: 20px 30px; background: #f8f9fa; color: #6b7280; font-size: 12px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">GESTÃO INOVA</div>
            <h1>{title}</h1>
        </div>
        <div class="body">
            {content}
        </div>
        <div class="footer">
            Este é um email automático do Sistema de Gestão InovaILab. Não responda a este email.
        </div>
    </div>
</body>
</html>"""


def send_meeting_invite(guests, title, description, date, start_time, end_time, organizer_name="Sistema"):
    """Envia convite de reunião por email para todos os guests."""
    content = f"""
    <p>Você foi convidado(a) para uma reunião:</p>
    <div class="info-box">
        <p><strong>📋 Título:</strong> {title}</p>
        <p><strong>📅 Data:</strong> {date}</p>
        <p><strong>🕐 Horário:</strong> {start_time} - {end_time}</p>
        <p><strong>👤 Organizador:</strong> {organizer_name}</p>
        {f'<p><strong>📝 Descrição:</strong> {description}</p>' if description else ''}
    </div>
    <p>Acesse o sistema para mais detalhes.</p>
    """
    html = _base_template(content, f"📅 Convite: {title}")
    success_count = 0
    errors = []
    last_err = None
    print(f"[email] send_meeting_invite chamado para {len(guests)} guests: {guests}")
    for guest_email in guests:
        if guest_email and '@' in guest_email:
            result = send_email(guest_email.strip(), f"Reunião: {title}", html)
            if result:
                success_count += 1
            else:
                errors.append(guest_email)
                last_err = _last_smtp_error
    print(f"[email] Resultado: {success_count} enviados, {len(errors)} falharam: {errors}, last_err={last_err}")
    return success_count, last_err


def send_notification_email(to, user_name, notification_title, notification_message, action_url=None):
    """Envia email de notificação genérica."""
    button_html = f'<a href="{action_url}" class="button">Acessar Sistema</a>' if action_url else ""
    content = f"""
    <p>Olá <strong>{user_name}</strong>,</p>
    <div class="info-box">
        <p><strong>{notification_title}</strong></p>
        <p>{notification_message}</p>
    </div>
    {button_html}
    """
    html = _base_template(content, notification_title)
    return send_email(to, notification_title, html)


def send_chamado_email(to, user_name, remetente_name, meeting_title, meeting_date, meeting_time, action_url):
    """Envia email de chamado (solicitação de reunião) com link para aceitar/recusar."""
    content = f"""
    <p>Olá <strong>{user_name}</strong>,</p>
    <p><strong>{remetente_name}</strong> solicitou sua participação em uma reunião:</p>
    <div class="info-box">
        <p><strong>📋 Reunião:</strong> {meeting_title}</p>
        <p><strong>📅 Data:</strong> {meeting_date}</p>
        <p><strong>🕐 Horário:</strong> {meeting_time}</p>
    </div>
    <p>Acesse o sistema para aceitar ou recusar:</p>
    <a href="{action_url}" class="button">Ver Notificação</a>
    """
    html = _base_template(content, "📬 Solicitação de Reunião")
    return send_email(to, f"Solicitação de Reunião: {meeting_title}", html)
