# Guia de Integração: FG Transcritor API + SMTP (Gmail)

> **Objetivo:** Este documento ensina como reproduzir, passo a passo, as integrações de **criação automática de reuniões com transcrição** (via FG Transcritor API) e **disparo de emails/notificações** (via SMTP Gmail) utilizadas no sistema OAZ 360. Foi escrito para que outra IA ou desenvolvedor consiga replicar 100% da funcionalidade em qualquer sistema Flask/Python.

---

## Sumário

1. [Variáveis de Ambiente (.env)](#1-variáveis-de-ambiente-env)
2. [Integração SMTP — Envio de Emails](#2-integração-smtp--envio-de-emails)
   - [Configuração do Gmail](#21-configuração-do-gmail)
   - [Serviço de Email (email.py)](#22-serviço-de-email-emailpy)
   - [Templates HTML](#23-templates-html)
   - [Funções Disponíveis](#24-funções-disponíveis)
   - [Onde os Emails São Disparados](#25-onde-os-emails-são-disparados)
   - [Como Usar em Outro Sistema](#26-como-usar-em-outro-sistema)
3. [Integração FG Transcritor — Criação de Reuniões](#3-integração-fg-transcritor--criação-de-reuniões)
   - [Sobre a API](#31-sobre-a-api)
   - [Autenticação](#32-autenticação)
   - [Endpoints da API](#33-endpoints-da-api)
   - [Client Python (fgtranscritor_client.py)](#34-client-python)
   - [Fluxo Completo de Criação de Reunião](#35-fluxo-completo-de-criação-de-reunião)
   - [Busca de Transcrição](#36-busca-de-transcrição)
   - [Análise com IA](#37-análise-com-ia)
   - [Como Usar em Outro Sistema](#38-como-usar-em-outro-sistema)
4. [Exemplo Prático Completo](#4-exemplo-prático-completo)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Variáveis de Ambiente (.env)

Abaixo estão **todas** as variáveis necessárias. Copie este bloco para o `.env` do novo sistema e preencha os valores:

```env
# ==============================
# SMTP / EMAIL (Gmail)
# ==============================
MAIL_USERNAME=hub@inovailab.com
MAIL_PASSWORD=suel ghmk hwyj zmuy
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_DEFAULT_SENDER=GESTÃOINOVA <noreply@inovailab.com.br>

# ==============================
# FG TRANSCRITOR (Reuniões + Transcrição)
# ==============================
FGTRANSCRITOR_API_KEY=fgtranscritorpass
FGTRANSCRITOR_HUB_EMAIL=hub@inovailab.com
FGTRANSCRITOR_BASE_URL=https://inovaimeet.com
FGTRANSCRITOR_COLLECTION_PATH=fgtranscritor_api.postman_collection.json
FGTRANSCRITOR_GET_TRANSCRIPT_PATH=/api/get_transcript

# Opcionais:
FGTRANSCRITOR_CREATE_MEETING_PATH=
FGTRANSCRITOR_AUTH_HEADER=X-API-Key
FGTRANSCRITOR_AUTH_SCHEME=
FGTRANSCRITOR_FORCE_URL=

# ==============================
# TRANSCRIÇÃO (TTL e refresh)
# ==============================
TRANSCRIPT_TTL_DAYS=7
TRANSCRIPT_CLEANUP_INTERVAL_HOURS=24
TRANSCRIPT_MIN_REFRESH_INTERVAL_SECONDS=15

# ==============================
# OPENAI (para análise da transcrição)
# ==============================
OPENAI_API_KEY=sk-proj-xxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

> **IMPORTANTE:**
> - `MAIL_PASSWORD` deve ser uma **Senha de App** do Google, **NÃO** a senha da conta.
> - `FGTRANSCRITOR_API_KEY` é a chave secreta que autentica suas chamadas à API do Transcritor.
> - `FGTRANSCRITOR_BASE_URL` é a URL base do serviço de transcrição (atualmente `https://inovaimeet.com`).

---

## 2. Integração SMTP — Envio de Emails

### 2.1 Configuração do Gmail

Para usar o Gmail como servidor SMTP, você precisa:

1. **Acessar** a conta Google com o email desejado (ex: `hub@inovailab.com`)
2. **Ativar verificação em duas etapas** em: [https://myaccount.google.com/security](https://myaccount.google.com/security)
3. **Criar uma Senha de App:**
   - Acesse: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Selecione "Outro (Nome personalizado)" → Nome: `OAZ360 SMTP`
   - Copie a senha gerada (formato: `xxxx xxxx xxxx xxxx`)
   - Cole no `.env` como `MAIL_PASSWORD`

> ⚠️ **Senha de App ≠ Senha da conta.** A Senha de App é uma senha de 16 caracteres gerada pelo Google especificamente para aplicações externas.

### 2.2 Serviço de Email (email.py)

O serviço de email é um módulo Python standalone, sem dependência de Flask-Mail ou outras bibliotecas externas. Usa apenas a biblioteca padrão `smtplib`.

**Arquivo:** `server_py/app/services/email.py`

**Estrutura:**

```python
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

# Configurações carregadas do .env
MAIL_SERVER   = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT     = int(os.getenv("MAIL_PORT", "587"))
MAIL_USE_TLS  = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "Sistema <noreply@sistema.com>")


def is_email_configured() -> bool:
    """Verifica se as credenciais SMTP estão preenchidas."""
    return bool(MAIL_USERNAME and MAIL_PASSWORD)


def send_email(to: str, subject: str, html_body: str, text_body: Optional[str] = None) -> bool:
    """
    Envia um email via SMTP.
    
    Args:
        to: Email do destinatário
        subject: Assunto do email
        html_body: Corpo HTML do email
        text_body: Corpo texto puro (fallback para clientes sem HTML)
    
    Returns:
        True se enviou com sucesso, False caso contrário.
    """
    if not is_email_configured():
        print(f"[email] SMTP não configurado, email não enviado para {to}")
        return False
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = MAIL_DEFAULT_SENDER
        msg["To"] = to
        
        if text_body:
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
        
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            if MAIL_USE_TLS:
                server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, to, msg.as_string())
        
        print(f"[email] Email enviado com sucesso para {to}: {subject}")
        return True
        
    except Exception as e:
        print(f"[email] Erro ao enviar email para {to}: {e}")
        return False
```

**Pontos-chave:**
- Usa `MIMEMultipart("alternative")` para enviar tanto HTML quanto texto puro.
- A conexão SMTP usa `STARTTLS` (porta 587) por padrão.
- O email é enviado a partir do `MAIL_USERNAME`, mas o remetente exibido é o `MAIL_DEFAULT_SENDER`.

### 2.3 Templates HTML

Todos os emails usam um template base HTML responsivo com:
- Gradiente roxo no header (`#667eea → #764ba2`)
- Caixas de informação com borda lateral azul
- Botões de ação estilizados
- Footer com aviso de email automático

**Template base (simplificado):**

```python
def _base_template(content: str, title: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; max-width: 600px; margin: auto; }}
        .container {{ background: white; border-radius: 8px; padding: 30px; }}
        .logo {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                 padding: 15px 25px; border-radius: 8px; font-size: 24px; font-weight: bold; }}
        .button {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white;
                   padding: 12px 30px; border-radius: 6px; text-decoration: none; }}
        .info-box {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; }}
        .credentials {{ background: #fff3cd; border: 1px solid #ffc107; padding: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><span class="logo">OAZ</span><h1>{title}</h1></div>
        {content}
        <div class="footer">Sistema de Avaliação 360° - OAZ</div>
    </div>
</body>
</html>
"""
```

### 2.4 Funções Disponíveis

| Função | Descrição | Parâmetros Obrigatórios |
|--------|-----------|------------------------|
| `send_welcome_email()` | Boas-vindas com credenciais de acesso | `to`, `user_name`, `password` |
| `send_cycle_started_email()` | Novo ciclo de avaliação iniciado | `to`, `user_name`, `cycle_name`, `cycle_type` |
| `send_timesheet_response_email()` | Timesheet respondido pelo colaborador | `to`, `gestor_name`, `user_name`, `timesheet_date` |
| `send_meeting_email()` | Convite para reunião 1v1 | `to`, `user_name`, `meeting_title`, `meeting_date`, `meeting_time`, `organizer_name` |
| `send_notification_email()` | Notificação genérica (qualquer mensagem) | `to`, `user_name`, `notification_title`, `notification_message` |

**Exemplo de uso direto:**

```python
from app.services.email import send_welcome_email, send_notification_email

# Enviar email de boas-vindas
send_welcome_email(
    to="joao@empresa.com",
    user_name="João Silva",
    password="senha_temporaria_123",
    login_url="https://oaz360.com.br/login"  # opcional, tem default
)

# Enviar notificação genérica
send_notification_email(
    to="maria@empresa.com",
    user_name="Maria",
    notification_title="Lembrete: Prazo de Avaliação",
    notification_message="Você tem 3 dias para completar sua autoavaliação.",
    login_url="https://oaz360.com.br/dashboard"  # opcional
)
```

### 2.5 Onde os Emails São Disparados

| Evento | Arquivo | Função de Email |
|--------|---------|-----------------|
| Usuário criado manualmente (Admin) | `routes/admin.py` | `send_welcome_email()` |
| Importação de planilha XLS | `services/import_xls.py` | `send_welcome_email()` |
| Ciclo de avaliação iniciado | `routes/admin_cycles.py` | `send_cycle_started_email()` |
| Timesheet respondido | `routes/timesheet.py` | `send_timesheet_response_email()` |
| Timesheet enviado para outro gestor | `routes/timesheet.py` | `send_notification_email()` |
| Notificação administrativa | `routes/admin.py` | `send_notification_email()` |

### 2.6 Como Usar em Outro Sistema

**Passo 1 — Copie o arquivo `email.py`** para o novo projeto:
```
novo_projeto/
├── app/
│   ├── services/
│   │   └── email.py       ← copiar este arquivo
│   └── ...
├── .env                    ← configurar MAIL_* aqui
└── ...
```

**Passo 2 — Configure o `.env`** com as credenciais do Gmail:
```env
MAIL_USERNAME=hub@inovailab.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_DEFAULT_SENDER=MeuSistema <noreply@meusistema.com>
```

**Passo 3 — Importe e use:**
```python
from dotenv import load_dotenv
load_dotenv()

from app.services.email import send_email, send_notification_email

# Email básico
send_email(
    to="usuario@email.com",
    subject="Teste de Email",
    html_body="<h1>Funcionou!</h1><p>Este é um teste.</p>"
)

# Ou use as funções prontas
send_notification_email(
    to="usuario@email.com",
    user_name="Fulano",
    notification_title="Bem-vindo!",
    notification_message="Sua conta foi criada com sucesso."
)
```

**Passo 4 — Verifique se funciona:**
```python
from app.services.email import is_email_configured
print(is_email_configured())  # True se MAIL_USERNAME e MAIL_PASSWORD estiverem preenchidos
```

---

## 3. Integração FG Transcritor — Criação de Reuniões

### 3.1 Sobre a API

O **FG Transcritor** (InovaiMeet) é um serviço que:
1. **Cria reuniões** com gravação e transcrição automática
2. **Grava** o áudio da reunião
3. **Transcreve** o áudio para texto
4. **Disponibiliza** a transcrição via API

A URL base atual é: `https://inovaimeet.com`

### 3.2 Autenticação

Todas as requests devem incluir o header de autenticação:

```
X-API-Key: fgtranscritorpass
```

**Variáveis envolvidas:**

| Variável | Descrição | Valor Atual |
|----------|-----------|-------------|
| `FGTRANSCRITOR_API_KEY` | Chave secreta de autenticação | `fgtranscritorpass` |
| `FGTRANSCRITOR_AUTH_HEADER` | Nome do header HTTP | `X-API-Key` |
| `FGTRANSCRITOR_AUTH_SCHEME` | Scheme opcional (ex: `Bearer`) | *(vazio = envia key diretamente)* |

**Lógica de autenticação:**
```python
# Se FGTRANSCRITOR_AUTH_SCHEME está vazio:
headers = {"X-API-Key": "fgtranscritorpass"}

# Se FGTRANSCRITOR_AUTH_SCHEME = "Bearer":
headers = {"X-API-Key": "Bearer fgtranscritorpass"}
```

### 3.3 Endpoints da API

#### 3.3.1 Criar Reunião (`POST /api/create_meeting`)

**URL:** `https://inovaimeet.com/api/create_meeting`

**Headers:**
```json
{
    "Content-Type": "application/json",
    "X-API-Key": "fgtranscritorpass"
}
```

**Body (JSON):**
```json
{
    "user_email": "hub@inovailab.com",
    "title": "Reunião 1v1 - João e Maria",
    "description": "Feedback do ciclo Janeiro 2026\n\n--- AGENDA ---\n1. Resultados\n2. Próximos passos",
    "start_time": "2026-02-15T14:00:00",
    "end_time": "2026-02-15T15:00:00",
    "attendees": ["joao@empresa.com", "maria@empresa.com"]
}
```

**Campos do Payload:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `user_email` | string | Sim | Email do hub/organizador (use `FGTRANSCRITOR_HUB_EMAIL`) |
| `title` | string | Sim | Título da reunião |
| `description` | string | Não | Descrição com agenda opcional |
| `start_time` | string (ISO 8601) | Sim | Data/hora de início (`YYYY-MM-DDTHH:MM:SS`) |
| `end_time` | string (ISO 8601) | Sim | Data/hora de término |
| `attendees` | array[string] | Sim | Lista de emails dos participantes |

**Resposta de Sucesso (200/201):**
```json
{
    "meeting_id": "abc123-uuid",
    "status": "created",
    "calendar_event_id": "...",
    "join_url": "https://inovaimeet.com/meeting/abc123"
}
```

**Resposta de Erro (4xx/5xx):**
```json
{
    "error": "Invalid API key",
    "message": "Unauthorized"
}
```

#### 3.3.2 Buscar Transcrição (`POST /api/get_transcript`)

**URL:** `https://inovaimeet.com/api/get_transcript`

**Headers:** (mesmos de criação)

**Body (JSON):**
```json
{
    "title": "Reunião 1v1 - João e Maria",
    "date": "2026-02-15"
}
```

**Campos do Payload:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `title` | string | Sim | Título exato da reunião (case-sensitive) |
| `date` | string | Sim | Data no formato `YYYY-MM-DD` |

**Resposta de Sucesso (200):**
```json
{
    "found": true,
    "transcription": "João: Bom dia Maria, vamos começar...\nMaria: Olá João..."
}
```

**Resposta Pendente (202/204):**
```json
{
    "status": "processing",
    "message": "Transcription is being processed"
}
```

**Resposta Não Encontrada (404):**
```json
{
    "found": false,
    "message": "No meeting found"
}
```

### 3.4 Client Python

Existem **dois** clients no projeto. O principal é `fgtranscritor_client.py`, que é mais robusto:

**Arquivo:** `server_py/app/integrations/fgtranscritor_client.py`

**Como ele resolve a URL do endpoint:**

```
Prioridade 1: FGTRANSCRITOR_BASE_URL + FGTRANSCRITOR_CREATE_MEETING_PATH (do .env)
Prioridade 2: URL extraída da Postman Collection + FGTRANSCRITOR_BASE_URL (override de domínio)
Prioridade 3: Fallback para https://inovaimeet.com/api/create_meeting
```

**Lógica de retry com variações de URL:**

O client tenta automaticamente múltiplas variações da URL para lidar com diferenças de path:
```python
def _build_url_variations(base_url: str) -> list[str]:
    # Ex: "https://inovaimeet.com/api/create_meeting"
    # Tenta:
    #   1. https://inovaimeet.com/api/create_meeting
    #   2. https://inovaimeet.com/api/create_meeting/
    #   3. https://inovaimeet.com/create_meeting      (sem /api)
    #   4. https://inovaimeet.com/create_meeting/
```

**Função principal — `create_meeting()`:**

```python
import requests
from flask import current_app

def create_meeting(payload: dict) -> dict:
    """
    Cria uma reunião no FG Transcritor.
    
    Args:
        payload: dict com user_email, title, description, start_time, end_time, attendees
    
    Returns:
        {"ok": True, "url": "...", "result": {...}} em caso de sucesso
        {"ok": False, "message": "...", "attempts": [...]} em caso de falha
    """
    api_key = current_app.config.get("FGTRANSCRITOR_API_KEY")
    if not api_key:
        raise RuntimeError("FGTRANSCRITOR_API_KEY is not configured")

    url = get_create_meeting_url()  # resolve a URL com fallback
    
    attempts = []
    for url_variation in _build_url_variations(url):
        try:
            response = requests.post(
                url_variation,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key
                },
                timeout=20,
            )
        except requests.RequestException as exc:
            attempts.append({"url": url_variation, "error": str(exc)})
            continue

        if response.status_code in (200, 201):
            return {"ok": True, "url": url_variation, "result": response.json()}
        
        attempts.append({
            "url": url_variation,
            "status": response.status_code,
            "snippet": response.text[:300],
        })
        if response.status_code != 404:
            break  # Só tenta variações se der 404

    return {"ok": False, "message": "Falha ao criar reuniao", "attempts": attempts}
```

### 3.5 Fluxo Completo de Criação de Reunião

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUXO DE CRIAÇÃO DE REUNIÃO                  │
│                                                                  │
│  1. Frontend envia POST /api/timesheet/entries/<id>/meeting      │
│     com: title, date, start_time, end_time, guests               │
│                                                                  │
│  2. Backend monta payload com attendees (emails dos envolvidos)  │
│     Payload: {user_email, title, description, start_time,        │
│               end_time, attendees}                               │
│                                                                  │
│  3. Backend chama fgtranscritor_client.create_meeting(payload)   │
│     → POST https://inovaimeet.com/api/create_meeting             │
│     → Header: X-API-Key: fgtranscritorpass                       │
│                                                                  │
│  4. API retorna meeting_id e detalhes                            │
│                                                                  │
│  5. Backend salva Meeting no banco local com:                    │
│     - provider: "fgtranscritor"                                  │
│     - provider_payload_json: (request enviado)                   │
│     - provider_response_json: (resposta recebida)                │
│     - transcript_source_title: (título para buscar transcrição)  │
│     - transcript_source_date: (data para buscar transcrição)     │
│     - status: "CREATED"                                          │
│                                                                  │
│  6. Depois da reunião acontecer, a transcrição fica disponível   │
│     via GET /api/get_transcript                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Rota da API (resumo):**

```python
# POST /api/timesheet/entries/<entry_id>/meeting
@bp.post("/api/timesheet/entries/<entry_id>/meeting")
@admin_or_gestor_required
def create_timesheet_meeting(entry_id: str):
    payload = request.get_json()
    
    # 1. Validar campos obrigatórios (date, start_time, end_time)
    # 2. Buscar usuários envolvidos (timesheet_user + manager)
    # 3. Montar lista de attendees (emails)
    # 4. Construir payload:
    request_payload = {
        "user_email": "hub@inovailab.com",     # FGTRANSCRITOR_HUB_EMAIL
        "title": "Título da reunião",
        "description": "Descrição + agenda",
        "start_time": "2026-02-15T14:00:00",
        "end_time": "2026-02-15T15:00:00",
        "attendees": ["gestor@email.com", "colaborador@email.com"]
    }
    
    # 5. Chamar API do Transcritor
    result = create_meeting(request_payload)
    
    # 6. Salvar Meeting no banco local
    if result.get("ok"):
        meeting = Meeting(
            title=title,
            start_at=start_dt, end_at=end_dt,
            provider="fgtranscritor",
            provider_payload_json=json.dumps(request_payload),
            provider_response_json=json.dumps(result.get("result")),
            status="CREATED",
            transcript_source_title=title,
            transcript_source_date=date_str,
        )
        db.add(meeting)
        db.commit()
```

### 3.6 Busca de Transcrição

Após a reunião acontecer, o sistema busca automaticamente a transcrição.

**Arquivo:** `server_py/app/services/transcription.py`

**Função principal — `fetch_transcription_from_fgtranscritor()`:**

```python
def fetch_transcription_from_fgtranscritor(meeting, attendees):
    """
    Busca a transcrição de uma reunião no FG Transcritor.
    
    A busca é feita por TÍTULO + DATA.
    O sistema tenta múltiplas variações de título:
      1. transcript_source_title (salvo na criação)
      2. title do meeting
      3. Títulos extraídos do provider_payload_json
      4. Títulos extraídos do provider_response_json
    
    Returns:
        {"status_code": 200, "text": "transcrição...", "pending": False, "error": None}
        {"status_code": 202, "text": None, "pending": True, "error": None}  # ainda processando
        {"status_code": 404, "text": None, "pending": False, "error": "not_found"}
    """
    url = f"{FGTRANSCRITOR_BASE_URL}/api/get_transcript"
    
    for title in title_candidates:
        response = requests.post(url, json={"title": title, "date": date_str},
                                  headers={"X-API-Key": api_key}, timeout=20)
        
        if response.status_code == 200:
            text = extract_transcription_text(response.json())
            if text:
                return {"status_code": 200, "text": text, "pending": False}
        
        if response.status_code == 202:  # Ainda processando
            return {"status_code": 202, "pending": True}
```

**Fluxo de refresh completo (`refresh_meeting_transcription`):**

```
1. Verifica intervalo mínimo entre tentativas (TRANSCRIPT_MIN_REFRESH_INTERVAL_SECONDS)
2. Verifica se já tem summary válido e não expirado
3. Se expirado (TRANSCRIPT_TTL_DAYS), limpa campos
4. Busca transcrição no FG Transcritor
5. Se encontrou texto, gera resumo analítico com OpenAI
6. Salva summary no banco com prazo de expiração
```

### 3.7 Análise com IA

Após obter a transcrição em texto, o sistema gera um resumo analítico usando OpenAI:

```python
def generate_transcript_analysis(transcription_text: str) -> str:
    prompt = (
        "Você é um analista sênior. Gere um resumo analítico em português, "
        "estruturado e acionável. Formato em markdown:\n"
        "## Decisões e acordos\n"
        "## Ações / tarefas acordadas (com responsáveis e prazos)\n"
        "## Riscos / impedimentos\n"
        "## Pontos de alinhamento/discordância\n"
        "## Perguntas abertas\n"
        "## Próximos passos recomendados\n\n"
        f"Transcrição:\n{transcription_text}"
    )
    return generate_completion(prompt, model_override=None,
                                system_message="Responda em português do Brasil.")
```

### 3.8 Como Usar em Outro Sistema

**Passo 1 — Instale as dependências:**
```bash
pip install requests python-dotenv openai
```

**Passo 2 — Copie os arquivos necessários:**
```
novo_projeto/
├── app/
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── fgtranscritor.py              ← client simples (opcional)
│   │   └── fgtranscritor_client.py       ← client principal
│   ├── services/
│   │   ├── transcription.py             ← busca + análise
│   │   └── email.py                     ← envio de emails
│   └── ...
├── fgtranscritor_api.postman_collection.json  ← collection da API
├── .env
└── ...
```

**Passo 3 — Configure o `.env`** (seção completa no início do documento).

**Passo 4 — Use diretamente (sem Flask):**

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FGTRANSCRITOR_API_KEY")
BASE_URL = os.getenv("FGTRANSCRITOR_BASE_URL", "https://inovaimeet.com")
HUB_EMAIL = os.getenv("FGTRANSCRITOR_HUB_EMAIL", "hub@inovailab.com")


def criar_reuniao(titulo, descricao, inicio, fim, participantes):
    """
    Cria uma reunião no FG Transcritor.
    
    Args:
        titulo: str - Título da reunião
        descricao: str - Descrição/agenda
        inicio: str - Data e hora de início (ISO 8601: "2026-02-15T14:00:00")
        fim: str - Data e hora de término (ISO 8601: "2026-02-15T15:00:00")
        participantes: list[str] - Lista de emails dos participantes
    
    Returns:
        dict com resultado da API
    """
    url = f"{BASE_URL}/api/create_meeting"
    
    payload = {
        "user_email": HUB_EMAIL,
        "title": titulo,
        "description": descricao,
        "start_time": inicio,
        "end_time": fim,
        "attendees": participantes,
    }
    
    response = requests.post(
        url,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
        timeout=20,
    )
    
    if response.status_code in (200, 201):
        print(f"✅ Reunião criada: {titulo}")
        return {"ok": True, "result": response.json()}
    else:
        print(f"❌ Erro {response.status_code}: {response.text[:200]}")
        return {"ok": False, "status": response.status_code, "error": response.text}


def buscar_transcricao(titulo, data):
    """
    Busca a transcrição de uma reunião.
    
    Args:
        titulo: str - Título exato da reunião
        data: str - Data no formato "YYYY-MM-DD"
    
    Returns:
        dict com transcrição ou status de pendência
    """
    url = f"{BASE_URL}/api/get_transcript"
    
    response = requests.post(
        url,
        json={"title": titulo, "date": data},
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
        timeout=20,
    )
    
    if response.status_code == 200:
        data = response.json()
        text = data.get("transcription") or data.get("transcript") or data.get("text")
        if text:
            return {"ok": True, "text": text}
    
    if response.status_code in (202, 204):
        return {"ok": False, "pending": True, "message": "Transcricao ainda processando"}
    
    return {"ok": False, "pending": False, "error": f"Status {response.status_code}"}


# ==========================================
# EXEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    # 1. Criar reunião
    resultado = criar_reuniao(
        titulo="Feedback Mensal - Equipe Dev",
        descricao="Reunião de feedback do mês de fevereiro\n\n--- AGENDA ---\n1. Resultados\n2. Metas",
        inicio="2026-02-15T14:00:00",
        fim="2026-02-15T15:00:00",
        participantes=["gestor@empresa.com", "dev@empresa.com"]
    )
    print(resultado)
    
    # 2. Buscar transcrição (depois que a reunião aconteceu)
    transcricao = buscar_transcricao(
        titulo="Feedback Mensal - Equipe Dev",
        data="2026-02-15"
    )
    print(transcricao)
```

---

## 4. Exemplo Prático Completo

Um script completo que cria uma reunião E envia email de notificação:

```python
#!/usr/bin/env python3
"""
Script standalone que demonstra ambas as integrações:
1. Cria uma reunião no FG Transcritor
2. Envia um email de notificação aos participantes

Uso:
    python3 exemplo_integracao_completa.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ---- Importar módulos ----
# Se usando como módulo dentro do projeto Flask:
#   from app.services.email import send_meeting_email
#   from app.integrations.fgtranscritor_client import create_meeting

# Se usando standalone (sem Flask), use as funções abaixo:
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_email_notificacao(destinatario, nome, titulo_reuniao, data, horario, organizador):
    """Envia email de convite para reunião."""
    mail_user = os.getenv("MAIL_USERNAME")
    mail_pass = os.getenv("MAIL_PASSWORD")
    mail_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    sender = os.getenv("MAIL_DEFAULT_SENDER", f"Sistema <{mail_user}>")
    
    if not mail_user or not mail_pass:
        print("[email] SMTP não configurado.")
        return False
    
    html = f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #667eea;">📅 Convite para Reunião</h2>
        <p>Olá <strong>{nome}</strong>,</p>
        <p>Você foi convidado(a) para uma reunião:</p>
        <div style="background: #f0f0ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
            <p><strong>Título:</strong> {titulo_reuniao}</p>
            <p><strong>Data:</strong> {data}</p>
            <p><strong>Horário:</strong> {horario}</p>
            <p><strong>Organizador:</strong> {organizador}</p>
        </div>
        <p>Acesse o sistema para mais detalhes.</p>
    </body></html>
    """
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Reunião: {titulo_reuniao}"
        msg["From"] = sender
        msg["To"] = destinatario
        msg.attach(MIMEText(html, "html", "utf-8"))
        
        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(mail_user, mail_pass)
            server.sendmail(mail_user, destinatario, msg.as_string())
        
        print(f"✅ Email enviado para {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False


def criar_reuniao_transcritor(titulo, descricao, inicio, fim, participantes):
    """Cria reunião no FG Transcritor."""
    api_key = os.getenv("FGTRANSCRITOR_API_KEY")
    base_url = os.getenv("FGTRANSCRITOR_BASE_URL", "https://inovaimeet.com")
    hub_email = os.getenv("FGTRANSCRITOR_HUB_EMAIL", "hub@inovailab.com")
    
    if not api_key:
        print("❌ FGTRANSCRITOR_API_KEY não configurada")
        return None
    
    response = requests.post(
        f"{base_url}/api/create_meeting",
        json={
            "user_email": hub_email,
            "title": titulo,
            "description": descricao,
            "start_time": inicio,
            "end_time": fim,
            "attendees": participantes,
        },
        headers={"Content-Type": "application/json", "X-API-Key": api_key},
        timeout=20,
    )
    
    if response.status_code in (200, 201):
        print(f"✅ Reunião criada: {titulo}")
        return response.json()
    else:
        print(f"❌ Erro ao criar reunião: {response.status_code} - {response.text[:200]}")
        return None


# ==========================================
# EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    PARTICIPANTES = ["gestor@empresa.com", "colaborador@empresa.com"]
    TITULO = "1v1 Feedback - Fevereiro 2026"
    DATA = "2026-02-15"
    INICIO = f"{DATA}T14:00:00"
    FIM = f"{DATA}T15:00:00"
    
    # 1. Criar reunião no Transcritor
    resultado = criar_reuniao_transcritor(
        titulo=TITULO,
        descricao="Feedback mensal\n\n--- AGENDA ---\n1. Performance\n2. Metas\n3. Próximos passos",
        inicio=INICIO,
        fim=FIM,
        participantes=PARTICIPANTES,
    )
    
    # 2. Enviar email para cada participante
    for email in PARTICIPANTES:
        enviar_email_notificacao(
            destinatario=email,
            nome=email.split("@")[0].title(),
            titulo_reuniao=TITULO,
            data=DATA,
            horario="14:00 - 15:00",
            organizador="Hub InovaiLab",
        )
    
    print("\n🎉 Integração completa executada com sucesso!")
```

---

## 5. Troubleshooting

### Email

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| `SMTP não configurado` | `MAIL_PASSWORD` vazio no `.env` | Gerar Senha de App no Google |
| `Authentication failed` | Senha errada ou conta sem 2FA | Verificar se usou Senha de App (não senha da conta) |
| `Connection refused` | Porta 587 bloqueada | Verificar firewall, testar porta 465 (SSL direto) |
| Email cai no spam | Sender diferente do login | Usar `MAIL_DEFAULT_SENDER` com o mesmo domínio |

### Transcritor

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| `FGTRANSCRITOR_API_KEY is not configured` | Variável ausente no `.env` | Adicionar `FGTRANSCRITOR_API_KEY=fgtranscritorpass` |
| `401 Unauthorized` | API Key inválida | Verificar se `FGTRANSCRITOR_API_KEY` está correta |
| `404 Not Found` | Endpoint errado | Verificar `FGTRANSCRITOR_BASE_URL` (deve ser `https://inovaimeet.com`) |
| Transcrição `not_found` | Título ou data não bate | A busca é por título exato + data. Conferir `transcript_source_title` |
| `connection timeout` | Serviço offline | Testar com `curl -X POST https://inovaimeet.com/api/create_meeting` |
| Transcrição `pending` | Reunião recente, ainda processando | Aguardar e retry (`TRANSCRIPT_MIN_REFRESH_INTERVAL_SECONDS`) |

---

## Resumo Rápido das Chaves

| Variável | Valor | Para quê |
|----------|-------|----------|
| `FGTRANSCRITOR_API_KEY` | `fgtranscritorpass` | Autenticação na API do Transcritor |
| `FGTRANSCRITOR_BASE_URL` | `https://inovaimeet.com` | URL base do serviço |
| `FGTRANSCRITOR_HUB_EMAIL` | `hub@inovailab.com` | Email organizador das reuniões |
| `MAIL_USERNAME` | `hub@inovailab.com` | Login SMTP Gmail |
| `MAIL_PASSWORD` | *(Senha de App Google)* | Senha SMTP |
| `MAIL_SERVER` | `smtp.gmail.com` | Servidor SMTP |
| `MAIL_PORT` | `587` | Porta SMTP (TLS) |
| `OPENAI_API_KEY` | `sk-proj-...` | Geração de resumo analítico da transcrição |

---

> **Nota Final:** Este documento contém todas as informações necessárias para reproduzir as integrações de email e transcritor em qualquer sistema Python/Flask. Basta copiar os arquivos indicados, configurar o `.env`, e seguir os exemplos de uso.
