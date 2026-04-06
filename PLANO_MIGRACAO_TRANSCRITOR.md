# Plano de Migração — Transcritor → Gestão

## Status
- Fase 1 iniciada: auditoria técnica comparativa
- Repositório auditado: `daniel-fgtranscritor`
- Repositório de destino: `FGinovaigestao`
- Diretriz fechada: **entram todas as variáveis do .env do Transcritor, exceto API principal, banco de dados e usuários/auth próprios**, porque o módulo final deve usar a base e o login do Gestão.

---

## Objetivo
Absorver o projeto **Transcritor** dentro do **FGinovaigestao**, transformando a aba atual de **Reuniões** em um módulo completo com subabas, sem duplicar autenticação, usuários ou banco de dados.

### Regras já decididas
1. O sistema final usa:
   - o **banco do Gestão**
   - a **OpenAI API key do Gestão**
   - os **usuários do Gestão**
2. O sistema final **não** mantém:
   - cadastro próprio de usuário do Transcritor
   - login/logout/register/verify-email próprios do Transcritor
   - banco separado do Transcritor
3. O sistema final **deve incorporar**:
   - telas/fluxos/templates do Transcritor adaptados ao layout do Gestão
   - Google Calendar / Google Meet
   - Fireflies
   - Gmail
   - demais integrações auxiliares do Transcritor
4. A aba principal continua sendo **Reuniões**, com subabas internas.

---

# Fase 1 — Auditoria Comparativa

## 1.1. O que existe hoje no Transcritor

### Backend principal
Arquivo principal: `daniel-fgtranscritor/app.py`

### Rotas principais identificadas
- `/`
- `/register`
- `/verify-email`
- `/resend-verification`
- `/users`
- `/login`
- `/logout`
- `/dashboard`
- `/meetings`
- `/new-meeting`
- `/analyze`
- `/meetings/<id>`
- `/meetings/<id>/delete`
- `/guest-analyze`
- `/results`
- `/new-analysis`
- `/live-demo`
- `/generate_agenda`
- `/edit_agenda`
- `/calendar`
- `/calendar/event/<id>`
- `/create_event`
- `/calendar/event/<id>/analyze`
- `/meetings/<id>/edit-calendar-analysis`
- `/meetings/<id>/process-calendar-analysis`
- `/settings`
- `/settings/google_calendar_connect`
- `/settings/google_callback`
- `/settings/google_calendar_disconnect`
- `/api/create_meeting`
- `/api/get_transcript`

### Templates identificados
- `dashboard.html`
- `meetings.html`
- `new_meeting.html`
- `results.html`
- `generate_agenda.html`
- `edit_agenda.html`
- `calendar.html`
- `event_details.html`
- `analyze_calendar_meeting.html`
- `settings.html`
- `users.html`
- `login.html`
- `register.html`
- `verify_email.html`
- `live_demo.html`

### Modelos identificados no Transcritor
#### `User`
Campos relevantes:
- `username`
- `email`
- `password_hash`
- `email_verified`
- `verification_code`
- `admin`
- `google_credentials`
- `google_calendar_enabled`

#### `Meeting`
Campos relevantes:
- `title`
- `agenda`
- `transcription`
- `language`
- `alignment_score`
- `meeting_date`
- `user_id`
- `results_json`
- `audio_url`
- `video_url`
- `google_calendar_event_id`
- `fireflies_transcript_id`

### Capacidades funcionais do Transcritor
1. criar reunião / análise
2. transcrever áudio
3. analisar reunião com IA
4. gerar pauta por IA
5. editar pauta antes do evento
6. integrar com Google Calendar
7. criar evento com Google Meet
8. buscar transcript/notas via Fireflies
9. expor API para criar reunião e buscar transcript
10. painel próprio de usuários/configurações

---

## 1.2. O que existe hoje no Gestão

### Módulo atual de reuniões
Arquivos identificados:
- `FGinovaigestao/routes_meetings.py`
- `FGinovaigestao/templates/meetings.html`
- `FGinovaigestao/templates/meeting_detail.html`
- `FGinovaigestao/models.py`

### Capacidades atuais do Gestão
#### `Meeting` do Gestão
Tabela atual: `meetings`

Campos atuais:
- `title`
- `date_time`
- `project_id`
- `transcription_id`
- `transcription_content`
- `analysis_summary`
- `created_at`
- `created_by_id`
- `status`
- participantes many-to-many

#### Fluxo atual
- listar reuniões
- filtrar por projeto/participante
- criar reunião simples
- ver detalhe
- mostrar transcrição/resumo simples

### Limitação atual do Gestão
O módulo atual é superficial comparado ao Transcritor:
- não tem fluxo robusto de pauta
- não tem pipeline completo de transcrição/análise
- não tem integração completa com Google Calendar
- não tem integração consolidada com Fireflies
- não tem subabas estruturadas

---

## 1.3. Conflitos identificados

### Conflito 1 — autenticação
O Transcritor tem login/registro próprios.

**Decisão:** não migra auth. Toda autenticação passa a usar o `User` do Gestão.

### Conflito 2 — modelo `User`
Os modelos não são compatíveis diretamente.

**Decisão:** usar o `User` do Gestão como fonte de verdade e migrar vínculo por `email`.

### Conflito 3 — modelo `Meeting`
Os dois projetos já têm `Meeting`, mas com estruturas diferentes.

**Decisão:** não coexistir com dois módulos separados; o `Meeting` do Gestão será expandido para absorver as capacidades do Transcritor.

### Conflito 4 — rotas `/meetings`
Ambos possuem rotas e templates de reuniões.

**Decisão:** o módulo do Gestão será substituído por uma versão evoluída, mantendo a navegação do Gestão e incorporando os fluxos do Transcritor.

### Conflito 5 — templates
Os templates do Transcritor usam `layout.html` próprio, diferente do `base.html` do Gestão.

**Decisão:** portar os templates para a base visual do Gestão, não copiar cruamente.

### Conflito 6 — credenciais por usuário
No Transcritor, credenciais Google vivem no `User`.

**Decisão recomendada:** mover isso para uma tabela de integrações por usuário no Gestão.

---

# Fase 2 — Arquitetura Alvo

## 2.1. Estratégia de incorporação
A incorporação será por **absorção modular**, não por cópia integral do app.

### Entram do Transcritor
- fluxos de análise de reunião
- geração de pauta
- edição de pauta
- calendário
- integração Google
- integração Fireflies
- serviços auxiliares
- templates convertidos
- endpoints internos reaproveitados/adaptados

### Não entram do Transcritor
- autenticação própria
- painel de usuários próprio
- `DATABASE_URL` próprio
- `OPENAI_API_KEY` própria
- criação de banco separado

---

## 2.2. Estrutura de navegação alvo
A aba principal continua sendo:
- **Reuniões**

### Subabas propostas
1. **Visão Geral**
2. **Todas as Reuniões**
3. **Nova Reunião / Nova Análise**
4. **Pautas**
5. **Calendário**
6. **Resultados / Análises**
7. **Integrações**

### Observação
A estrutura pode ser refinada em implementação, mas o conceito é:
- uma aba principal no menu do Gestão
- navegação interna do módulo por subabas

---

## 2.3. Modelo alvo de dados

### Estratégia escolhida
Expandir o `Meeting` do Gestão, em vez de manter um `Meeting` paralelo.

### Campos a adicionar em `meetings`
Proposta inicial:
- `agenda` (`Text`)
- `transcription` (`Text`) — ou reaproveitar `transcription_content`
- `language` (`String(10)`)
- `alignment_score` (`Float`)
- `results_json` (`Text`)
- `audio_url` (`String(5000)`)
- `video_url` (`String(5000)`)
- `google_calendar_event_id` (`String(255)`)
- `fireflies_transcript_id` (`String(255)`)
- `external_meeting_link` (`String(1000)`, opcional)
- `analysis_status` (`String(30)`, opcional)
- `analysis_generated_at` (`DateTime`, opcional)

### Compatibilização de campos existentes
#### Gestão atual
- `transcription_content`
- `analysis_summary`

#### Alvo
- manter compatibilidade com o que já existe
- decidir em implementação se:
  - `transcription_content` vira o campo principal de transcrição
  - `analysis_summary` continua como resumo rápido derivado de `results_json`

### Tabela nova recomendada
#### `user_calendar_integrations` (nome provisório)
Campos sugeridos:
- `id`
- `user_id`
- `provider` (`google` inicialmente)
- `credentials_json`
- `enabled`
- `created_at`
- `updated_at`

**Motivo:** não poluir `User` e preparar base para integrações futuras.

---

# Fase 3 — Variáveis de Ambiente

## Regra fechada pelo usuário
Entram **todas as variáveis do .env do Transcritor**, exceto:
- API principal do Transcritor (usa a do Gestão)
- banco de dados do Transcritor (usa o do Gestão)
- usuários/auth próprios

## Variáveis a incorporar no Gestão
### Google / OAuth
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `REDIRECT_URI`

### Gmail
- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`
- `GMAIL_REFRESH_TOKEN`
- `GMAIL_SENDER_EMAIL`

### Fireflies
- `FIREFLIES_API_TOKEN`

### Azure / Microsoft
- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `MSAL_REDIRECT_URI`
- `AZURE_CLIENT_SECRET`

### Sessão/segurança complementar
- `API_SECRET_KEY`

### Observação importante
As credenciais reais foram disponibilizadas fora do código durante a conversa e **não devem ser committedas em repositório**. A incorporação deve acontecer via `.env`/secret manager do ambiente do Gestão.

---

# Fase 4 — Migração de Usuários e Dados

## 4.1. Usuários
### Estratégia
Mapear usuários do Transcritor para usuários do Gestão por `email`.

### Regras
1. `email` é a chave de reconciliação
2. IDs do Transcritor não serão preservados como fonte de verdade
3. Se algum e-mail do Transcritor não existir no Gestão:
   - registrar em relatório de pendências
   - decidir manualmente criar ou reatribuir

---

## 4.2. Reuniões
### Estratégia
Migrar reuniões antigas do banco do Transcritor para o banco do Gestão após o schema alvo estar pronto.

### Campos candidatos à migração
- título
- agenda
- transcrição
- idioma
- score de alinhamento
- data da reunião
- criador
- resultados JSON
- links de áudio/vídeo
- ID de evento Google
- ID Fireflies

### Cuidados
- converter `user_id` pelo e-mail correspondente
- manter relação com projeto apenas se existir mapeamento seguro
- reuniões sem vínculo de projeto podem entrar como reuniões soltas

---

## 4.3. Credenciais Google por usuário
Se houver credenciais ativas no Transcritor:
- extrair de `user.google_credentials`
- converter para a nova tabela de integrações do Gestão
- marcar `enabled` quando aplicável

---

# Fase 5 — Backend de Implementação

## 5.1. Organização proposta
Criar um módulo de reuniões v2 no Gestão, reaproveitando código do Transcritor em camadas:

### Arquivos/áreas novas sugeridas
- `services/meetings_ai_service.py`
- `services/meetings_calendar_service.py`
- `services/meetings_fireflies_service.py`
- `services/meetings_gmail_service.py`
- `routes_meetings.py` (expandido) ou `routes_meetings_v2.py`

### Regra de ouro
Não manter serviços duplicados com lógica equivalente em dois lugares se puder unificar.

---

## 5.2. Ordem técnica recomendada
1. preparar migrations
2. criar tabela de integrações
3. expandir `Meeting`
4. portar serviços de IA/transcrição
5. portar Google Calendar
6. portar Fireflies
7. portar Gmail
8. adaptar rotas
9. adaptar templates
10. migrar dados
11. ativar UI final

---

# Fase 6 — Frontend / Templates

## Estratégia
Portar o conteúdo do Transcritor para o layout do Gestão.

### Conversões necessárias
- `layout.html` do Transcritor → `base.html` do Gestão
- ações em páginas separadas → subabas/componentes do módulo Reuniões
- formulários e tabelas adaptados ao estilo do Gestão

### Templates fonte a reaproveitar
- `meetings.html`
- `new_meeting.html`
- `results.html`
- `generate_agenda.html`
- `edit_agenda.html`
- `calendar.html`
- `event_details.html`
- `analyze_calendar_meeting.html`
- `settings.html`

### Templates que não migram como produto final
- `login.html`
- `register.html`
- `verify_email.html`
- `users.html`

Esses podem servir só como referência funcional, mas não entram no módulo final.

---

# Fase 7 — Estratégia de Deploy Seguro

## 7.1. Implantação por etapas
### Etapa A — estrutura invisível
- migrations
- services
- integrações
- rotas internas

### Etapa B — feature flag
Adicionar algo como:
- `MEETINGS_V2_ENABLED=true`

### Etapa C — homologação
Validar:
- criação de reunião
- geração de pauta
- edição de pauta
- transcrição
- análise
- calendário
- Fireflies
- vinculação de usuários

### Etapa D — virada
Trocar a aba atual de Reuniões para apontar para o módulo novo.

### Etapa E — limpeza
Remover código morto do hub antigo.

---

# Riscos e Cuidados

## Riscos altos
1. conflito entre o `Meeting` atual e o `Meeting` absorvido
2. migração incorreta de usuários por ID ao invés de e-mail
3. templates do Transcritor colados sem adaptação ao layout do Gestão
4. callback OAuth configurado errado no domínio final
5. uso de credenciais sensíveis direto no código/repo
6. dependências novas quebrando o ambiente atual
7. deploy parcial deixando a aba Reuniões inconsistente

## Mitigações
- migrations incrementais
- feature flag
- reconciliação por e-mail
- testes por fluxo
- segredos só em `.env`
- homologação antes da virada

---

# Próximos Passos Imediatos

## Fase 1.1 concluída parcialmente
Já auditado:
- rotas principais do Transcritor
- modelos principais do Transcritor
- módulo atual de reuniões do Gestão
- conflito central de autenticação e modelo de reuniões
- famílias de variáveis `.env` a incorporar

## Próxima execução imediata
### Fase 1.2
Aprofundar leitura de:
- `new_meeting.html`
- `results.html`
- `calendar.html`
- `settings.html`
- serviços auxiliares (`gmail_service.py`, `google_calendar.py`, `calendar_utils.py`)

### Fase 2
Desenhar schema final de `Meeting` + tabela de integrações

### Fase 3
Preparar lista de migrations SQLAlchemy/Alembic para começar a implementação

### Fase 3.1 — Base de migração criada
Arquivo criado:
- `scripts/import_transcritor_data.py`

Escopo inicial do script:
- conectar no banco do Transcritor por `--source-url`
- ler usuários fonte
- ler reuniões fonte
- reconciliar usuários por email com o banco do Gestão
- importar credenciais Google para `user_integration_credentials`
- importar reuniões para `meetings`
- preservar IDs externos (`google_calendar_event_id`, `fireflies_transcript_id`)
- suportar `--dry-run`
- suportar `--limit`

---

# Fase 2 — Desenho Técnico Detalhado

## 2.4. Leitura aprofundada dos templates do Transcritor

### `new_meeting.html`
Representa o fluxo de **nova análise manual**:
- título da reunião
- data opcional
- pauta
- transcrição completa
- submissão para análise direta

**Conclusão:** esse fluxo deve virar uma subaba do Gestão chamada algo como **Nova análise** e pode conviver com criação de reunião de calendário.

### `results.html`
É o template mais rico do Transcritor e concentra a entrega de valor.

#### Blocos funcionais identificados
- resumo executivo da reunião
- score de alinhamento
- régua visual de qualidade/alinhamento
- cobertura da pauta
- itens abordados / não abordados
- tópicos adicionais
- insights
- próximos passos
- action items
- direções estratégicas
- aba separada para transcrição
- enriquecimento opcional com dados do Fireflies

**Conclusão:** este template deve ser a base do **detalhe avançado da reunião** no Gestão.

### `calendar.html`
Representa o módulo de agenda/conexão com Google Calendar.

#### Blocos funcionais identificados
- próxima reunião
- reuniões recentes
- atalho para configurações
- atalho para gerar pauta com IA
- modal rico para criação de evento
- suporte a recorrência
- suporte a participantes
- fluxo orientado a agenda operacional, não apenas análise

**Conclusão:** o Gestão precisa ganhar uma subaba própria de **Calendário** e não só uma listagem simples de reuniões internas.

### `settings.html`
Representa um painel de integrações por usuário.

#### Blocos funcionais identificados
- status da conta
- status da integração Google Calendar
- conectar/desconectar conta Google
- acesso aos próprios eventos

**Conclusão:** no Gestão isso deve virar a subaba **Integrações**, ligada ao usuário logado do Gestão.

---

## 2.5. Serviços técnicos auditados

### `gmail_service.py`
Capacidade identificada:
- envio de e-mail via Gmail API usando OAuth2 e refresh token
- dependência direta de:
  - `GMAIL_CLIENT_ID`
  - `GMAIL_CLIENT_SECRET`
  - `GMAIL_REFRESH_TOKEN`
  - `GMAIL_SENDER_EMAIL`

**Decisão:** incorporar ao Gestão como serviço auxiliar do módulo Reuniões/Comunicação.

### `calendar_utils.py`
Capacidade identificada:
- wrappers para Google OAuth/Calendar
- criação de evento com recorrência
- criação de conferenceData/Meet

**Decisão:** incorporar como camada de serviço, evitando dependência direta das rotas com o provider.

### `google_calendar.py` / `google_calendar_integration.py`
Capacidade identificada:
- OAuth Google
- troca de code por credenciais
- renovação de token
- listagem de eventos
- construção do service do Google Calendar

**Decisão:** consolidar isso no Gestão em um serviço único de integração Google.

---

## 2.6. Estrutura alvo de subabas no Gestão

### Aba principal: `Reuniões`
Subabas propostas para implementação:

1. **Visão Geral**
   - KPIs rápidos
   - próximas reuniões
   - reuniões recentes
   - atalhos principais

2. **Todas as Reuniões**
   - listagem
   - filtros por projeto, participante, status, origem, período

3. **Nova Análise**
   - fluxo manual do `new_meeting.html`
   - pauta + transcrição + análise direta

4. **Pautas**
   - gerar pauta com IA
   - editar pauta
   - opcionalmente associar a projeto/reunião

5. **Calendário**
   - integração Google Calendar
   - próxima reunião
   - reuniões recentes
   - criação de evento com Meet
   - recorrência

6. **Resultados**
   - visualização rica tipo `results.html`
   - tabs de análise / transcrição / ações / direções

7. **Integrações**
   - status da conexão Google
   - ações de conectar/desconectar
   - futuramente Fireflies/Microsoft

---

## 2.7. Schema alvo detalhado

### Estratégia definitiva desta fase
**Expandir o `Meeting` do Gestão** e manter uma tabela separada para integrações por usuário.

## 2.7.1. Modelo `Meeting` alvo
Tabela existente: `meetings`

### Campos já existentes no Gestão
- `id`
- `title`
- `date_time`
- `project_id`
- `transcription_id`
- `transcription_content`
- `analysis_summary`
- `created_at`
- `created_by_id`
- `status`

### Campos a adicionar
- `agenda` (`Text`, nullable=True)
- `language` (`String(10)`, nullable=True)
- `alignment_score` (`Float`, nullable=True)
- `results_json` (`Text`, nullable=True)
- `audio_url` (`String(5000)`, nullable=True)
- `video_url` (`String(5000)`, nullable=True)
- `google_calendar_event_id` (`String(255)`, nullable=True, index=True)
- `fireflies_transcript_id` (`String(255)`, nullable=True, index=True)
- `external_meeting_link` (`String(1000)`, nullable=True)
- `meeting_source` (`String(30)`, nullable=False, default='internal')`
- `analysis_status` (`String(30)`, nullable=False, default='pending')`
- `analysis_generated_at` (`DateTime`, nullable=True)
- `meeting_owner_email` (`String(255)`, nullable=True)
- `raw_provider_payload` (`Text`, nullable=True)

### Campos a preservar e reinterpretar
- `transcription_content` permanece como campo principal de transcrição textual
- `analysis_summary` permanece como resumo curto renderizável no hub
- `transcription_id` pode ser mantido por compatibilidade, mas idealmente será descontinuado em favor de IDs explícitos (`fireflies_transcript_id` etc.)

## 2.7.2. Tabela nova: integrações por usuário
### Nome sugerido
`user_integration_credentials`

### Campos sugeridos
- `id`
- `user_id` (`FK user.id`, index)
- `provider` (`String(50)`) — ex.: `google_calendar`, `fireflies`, `microsoft`
- `account_email` (`String(255)`, nullable=True)
- `credentials_json` (`Text`, nullable=True)
- `is_enabled` (`Boolean`, default=True)
- `created_at` (`DateTime`)
- `updated_at` (`DateTime`)
- `last_sync_at` (`DateTime`, nullable=True)
- `meta_json` (`Text`, nullable=True)

### Regras
- um usuário pode ter múltiplas integrações
- provider + user_id deve ser único por padrão para Google Calendar, salvo futura necessidade multi-conta

## 2.7.3. Tabela opcional futura
### `meeting_ai_artifacts`
Se o volume de dados crescer, podemos extrair blobs/artefatos do `Meeting` depois.

**Nesta fase:** não necessário. Primeiro consolidar no `meetings` para acelerar incorporação.

---

## 2.8. Lista de migrations necessárias

### Migration 1 — expandir `meetings`
Adicionar colunas:
- `agenda`
- `language`
- `alignment_score`
- `results_json`
- `audio_url`
- `video_url`
- `google_calendar_event_id`
- `fireflies_transcript_id`
- `external_meeting_link`
- `meeting_source`
- `analysis_status`
- `analysis_generated_at`
- `meeting_owner_email`
- `raw_provider_payload`

### Migration 2 — criar tabela `user_integration_credentials`
Criar tabela e índices.

### Migration 3 — constraints e índices
- índice em `google_calendar_event_id`
- índice em `fireflies_transcript_id`
- índice composto eventual em `provider, user_id`

### Migration 4 — backfill inicial
- popular `meeting_source='internal'` para registros existentes
- popular `analysis_status='pending'` para registros existentes

### Migration 5 — migração de credenciais antigas (quando houver dados)
- importar `google_credentials` do banco do Transcritor para `user_integration_credentials`

---

## 2.9. Mapa de incorporação arquivo por arquivo

### Entram como base funcional
- `openai_service.py` → reaproveitar lógica de análise/transcrição/pauta, mas idealmente fundir em serviços do Gestão
- `google_calendar.py`
- `google_calendar_integration.py`
- `calendar_utils.py`
- `gmail_service.py`

### Entram como referência de interface e fluxo
- `templates/new_meeting.html`
- `templates/results.html`
- `templates/calendar.html`
- `templates/edit_agenda.html`
- `templates/generate_agenda.html`
- `templates/event_details.html`
- `templates/analyze_calendar_meeting.html`
- `templates/settings.html`
- `templates/meetings.html`

### Não entram como produto final
- `templates/login.html`
- `templates/register.html`
- `templates/verify_email.html`
- `templates/users.html`
- rotas `/login`, `/logout`, `/register`, `/verify-email`, `/users`

### Devem ser reescritos/adaptados no Gestão
- `app.py` do Transcritor não deve ser transplantado; apenas sua lógica funcional deve ser repartida entre:
  - models do Gestão
  - services do Gestão
  - rotas do Gestão
  - templates do Gestão

---

## 2.10. Ordem de implementação da fase técnica

### Etapa 1
Criar os models novos/expandidos:
- expandir `Meeting`
- criar `UserIntegrationCredential`

### Etapa 2
Criar migrations reais no Gestão.

### Etapa 3
Portar serviços:
- análise/transcrição
- geração de pauta
- Google Calendar
- Fireflies
- Gmail

### Etapa 4
Refazer `routes_meetings.py` para suportar subabas.

### Etapa 5
Portar templates para `base.html`.

### Etapa 6
Migrar dados antigos do Transcritor.

### Etapa 7
Virar a navegação principal de Reuniões para o módulo novo.

---

# Decisão Operacional Atual
A incorporação vai seguir a seguinte linha:

1. **absorver o Transcritor para dentro do Gestão**
2. **usar banco, usuários e OpenAI do Gestão**
3. **incorporar o restante do .env do Transcritor**
4. **substituir o módulo atual de Reuniões por uma versão expandida**
5. **migrar dados por e-mail, não por ID bruto**
6. **adaptar os templates do Transcritor como subabas no layout do Gestão**

---

## Observação final
Este documento é o plano mestre da migração. A partir daqui, a próxima etapa é detalhar o schema final e iniciar a implementação por fases, sem improviso e sem mistura de dois sistemas concorrentes de reuniões.
