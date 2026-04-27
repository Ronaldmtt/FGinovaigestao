# FGinovaigestao

Plataforma web monolítica em Flask para operação interna da Inovai, unificando **gestão de projetos**, **tarefas/Kanban**, **reuniões com IA**, **CRM/CRM2**, **financeiro PJ**, **arquivos**, **integrações GitHub/Google/Fireflies** e **API própria para automações**.

## Visão geral

O sistema funciona como uma central operacional dark mode para acompanhar o ciclo completo de trabalho da empresa:

- entrada e qualificação de leads
- reuniões comerciais e operacionais
- geração de pautas e análises com IA
- abertura e acompanhamento de projetos
- gestão de tarefas e to-dos em Kanban
- documentação e arquivos por projeto
- integração com GitHub para contexto técnico
- módulo financeiro PJ para contas, centros de custo, metas e lançamentos
- exposição de dados via API keys por projeto ou por sistema
- monitoramento de automações/RPA

Na prática, ele tenta concentrar em um único produto o que normalmente ficaria espalhado entre CRM, agenda, PM tool, notas de reunião, financeiro e integrações técnicas.

---

## Objetivo do sistema

O FGinovaigestao foi construído para resolver um problema operacional real: projetos, leads, reuniões e tarefas ficavam fragmentados entre planilhas, conversas, ferramentas isoladas e memória da equipe.

O sistema organiza isso em um fluxo único:

1. o lead entra
2. passa por CRM / CRM2
3. pode gerar reuniões e análises
4. vira cliente/projeto
5. o projeto ganha escopo, contexto, arquivos, integrações e equipe
6. tarefas e to-dos são gerados/manualizados
7. o Kanban acompanha a execução
8. o financeiro acompanha contas, despesas, metas e relatórios
9. a API expõe tudo para integrações externas

---

## Stack e arquitetura

## Backend
- Python 3
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Mail

## Frontend
- Jinja2 server-side rendering
- Bootstrap dark theme
- Font Awesome
- JavaScript vanilla para interações, filtros, drawers, drag-and-drop e painéis dinâmicos

## Banco
- compatível com SQLite e PostgreSQL
- várias migrações incrementais feitas diretamente no startup e por scripts auxiliares

## Infra e operação
- Gunicorn
- ProxyFix
- serviço systemd (`gestao_app.service`)
- configuração para Nginx (`nginx_gestao_app.conf`)

## Integrações
- OpenAI
- GitHub API
- Google Calendar / Google Meet
- Fireflies
- SMTP/Gmail
- WebSocket/RPA Monitor

## Estilo arquitetural
É um **monólito modular**.

Arquivos principais:
- `app.py` → bootstrap, config, DB, uploads, mail, migrações leves no startup
- `routes.py` → maior parte das rotas principais do produto
- `routes_meetings.py` → hub de reuniões e integrações de agenda/transcrição
- `routes_financeiro.py` → módulo financeiro PJ
- `api_v1.py` → API autenticada por chaves
- `models.py` → modelos relacionais centrais
- `services/` → integrações e serviços de reuniões/IA

---

## Módulos do sistema

## 1. Dashboard
Rota principal: `/dashboard`

Entrega visão executiva do sistema com:
- métricas gerais ou personalizadas por usuário
- total de projetos, tarefas, clientes e pendências
- cards por status de projeto
- atalhos rápidos
- atividades recentes
- ferramentas administrativas para exportação/importação

O dashboard muda conforme o perfil:
- **admin** vê números globais
- **usuário comum** vê seus projetos, tarefas e clientes criados

---

## 2. Usuários e permissões
Rotas principais:
- `/admin/users`
- `/admin/users/new`
- `/admin/users/edit/<id>`

O sistema tem autenticação por login/senha e controle de acesso granular.

### O que existe
- usuário admin e usuário comum
- ativação/desativação de usuário
- recuperação e troca de senha
- último acesso
- preferência de notificação por e-mail
- token pessoal do GitHub por usuário

### Permissões por módulo
Cada usuário pode ter acesso individual a:
- clientes
- projetos
- tarefas
- kanban
- CRM
- usuários
- financeiro
- reuniões
- relatórios
- API do sistema

Isso permite transformar o app em uma central interna com acesso segmentado.

---

## 3. Clientes
Rotas principais:
- `/clients`
- `/clients/new`
- `/clients/edit/<id>`
- `/clients/<id>/generate-public-link`

### O módulo faz
- cadastro e edição de clientes
- dados básicos, empresa, observações, contato
- vínculo do cliente com projetos
- geração de **código público** para acesso externo

### Diferencial
Existe um fluxo de **acesso público** para o cliente acompanhar informações sem login interno.

Rotas públicas relevantes:
- `/public`
- `/public/timeline/<code>`
- `/public/project-details/<project_id>/<code>`
- `/public/project-tasks/<project_id>/<code>`
- `/public/project-stats/<project_id>/<code>`

Isso indica um mini-portal do cliente para transparência operacional.

---

## 4. Projetos
Rotas principais:
- `/projects`
- `/projects/new`
- `/projects/new-manual`
- `/projects/<id>`
- `/projects/<id>/edit`
- `/projects/<id>/process-ai`
- `/projects/<id>/status-history`

Esse é o núcleo do produto.

### O projeto guarda
- nome
- cliente vinculado
- responsável interno
- equipe do projeto
- status
- progresso
- datas de início, prazo e entrega
- responsável do lado do cliente
- repositório GitHub
- domínio
- servidor SSH / VPS
- path SSH
- identificador de RPA
- estrutura de escopo e contexto
- transcrição original
- flags técnicas (`has_github`, `has_drive`, `has_env`, `has_backup_db`)

### Status do projeto
Há mais de um estado operacional, incluindo:
- em andamento
- em teste
- pausado
- cancelado
- concluído

### Histórico de status
Cada mudança pode ser registrada em `ProjectStatusHistory`, o que permite trilha de evolução do projeto.

### Projetos vinculados
O sistema suporta relação **pai/filho** entre projetos.

Isso permite modelar:
- projeto principal + fases
- projeto principal + subprojetos
- entregas relacionadas

Na UI isso aparece como carrossel de projetos vinculados.

### Abas do detalhe do projeto
Na tela `project_detail.html` o projeto é organizado por abas como:
- **Detalhes**
- **Arquivos**
- **API**
- **GitHub** (quando aplicável)

### O que existe na aba Detalhes
- contexto e justificativa
- problema/oportunidade
- objetivos
- alinhamento estratégico
- escopo do projeto
- fora do escopo
- premissas
- restrições
- transcrição original
- equipe do projeto
- tarefas relacionadas

### Botões/ações do projeto
- nova reunião
- editar projeto
- deletar projeto
- processar transcrição com IA
- abrir histórico de status
- ver no Kanban
- abrir dados e commits do GitHub

---

## 5. IA aplicada a projeto
Rotas/serviços relevantes:
- `/projects/<id>/process-ai`
- `openai_service.py`
- `ai_analysis_service.py`
- `ai_copilot.py`

A IA não está só como chatbot. Ela participa do fluxo de trabalho.

### Casos de uso presentes
- transformar transcrição em escopo estruturado
- preencher automaticamente campos do projeto
- gerar tarefas a partir de transcrição
- gerar análises e resumos
- gerar contexto técnico a partir de reunião + repo

### Resultado prático
O sistema reduz tempo de setup de projeto e formaliza briefing operacional/comercial com menos trabalho manual.

---

## 6. Tarefas
Rotas principais:
- `/tasks`
- `/tasks/new`
- `/tasks/new-manual`
- `/tasks/transcription`
- `/tasks/<task_id>/edit`
- `/tasks/<task_id>/data`

### O módulo permite
- criar tarefa simples
- criar tarefa manual mais detalhada
- gerar tarefas com IA
- vincular tarefa a projeto e usuário
- definir prazo
- alterar status
- listar com filtros por projeto, cliente, usuário e status

### Campos principais da tarefa
- título
- descrição
- projeto
- responsável
- data de conclusão
- status
- ordem no kanban
- marcação de disparo

### To-dos internos
Cada tarefa pode ter vários `TodoItem`.

Isso transforma a tarefa em um container com checklist executável.

### Ações importantes
- editar tarefa
- deletar
- atualizar status
- reordenar
- disparar tarefa
- gerar to-dos a partir de commits do GitHub

---

## 7. Kanban
Rota principal: `/kanban`

O Kanban é um dos módulos mais ricos visualmente.

### O que faz
- mostra tarefas em colunas por status
- permite filtros por cliente, projeto e relações
- aceita criação rápida de tarefas
- aceita inclusão de transcrição
- possui drag-and-drop / reordenação
- exibe sinais visuais fortes para urgência e estados

### Regras operacionais
O código deixa claro que só projetos **em andamento** podem receber novas demandas no Kanban.

### Sinais visuais
Há uma camada visual premium com glow e estados semânticos, especialmente para:
- urgência
- bloqueio
- prioridade
- badges de to-dos
- notificações

O Kanban tem papel de execução, não só de consulta.

---

## 8. Reuniões
Rotas principais:
- `/meetings`
- `/meetings/<meeting_id>`
- `/meetings/analyze`
- `/meetings/agenda/generate`
- `/meetings/calendar/create`
- `/meetings/sync-google`
- `/meetings/<meeting_id>/sync-fireflies`

O módulo de reuniões é praticamente um subproduto dentro da plataforma.

### O hub de reuniões cobre
- visão geral de reuniões
- listagem completa
- nova análise manual
- criação de nova reunião
- agenda/calendário
- integrações

### Capacidades do módulo
- criar reunião manualmente
- gerar pauta com IA
- conectar Google Calendar
- criar evento com Meet
- sincronizar eventos do Google
- importar evento já existente
- sincronizar transcrição do Fireflies
- analisar a reunião com IA
- consolidar resumo, alinhamento, ações e notas

### O que existe no detalhe da reunião
Pelos serviços e templates, há suporte para:
- transcrição estruturada por speaker
- resumo
- action items
- notas
- alinhamento com pauta
- status da reunião
- origem da reunião (interna / Google Calendar)
- payload bruto do provedor

### Objetivo real desse módulo
Ele fecha o gap entre reunião comercial/operacional e execução do projeto.

---

## 9. CRM clássico
Rotas principais:
- `/crm`
- `/crm/contato/novo`
- `/crm/contato/<id>`
- `/crm/contato/<id>/editar`
- `/crm/contato/<id>/mudar-estagio`
- `/crm/contato/<id>/comentario`

### Funções
- cadastro de contatos/leads
- pipeline por estágio
- observações e comentários
- sync de leads do site
- arquivos anexos por contato
- edição e deleção

### Entidades relacionadas
- `Contato`
- `Comentario`
- `ContatoFile`
- `CrmStage`

É um CRM mais simples, focado em operação.

---

## 10. CRM2 / Pipeline comercial avançado
Rotas principais:
- `/crm2/leads`
- `/crm2/pipeline`
- `/crm2/lead/<lead_id>`
- `/crm2/notifications`
- várias rotas `/api/crm2/...`

Esse módulo é mais sofisticado e parece representar a evolução do CRM.

### O que ele cobre
- leads estruturados
- pipeline visual em colunas
- drag-and-drop de estágio
- detalhamento do lead
- reuniões vinculadas ao lead
- notificações internas
- geração de pauta
- proposta
- contrato
- aceite/rejeição
- conversão para cliente
- abertura de chamado

### Estágios observados
No pipeline aparecem estágios como:
- Captação
- Bloco 1
- Bloco 2
- Proposta
- Contrato
- Cliente

### O que isso significa
O sistema acompanha o lead do primeiro contato até virar cliente formal.

### Itens relevantes
- `Crm2Lead`
- `Crm2Meeting`
- `Crm2Notification`
- `Crm2Proposal`
- `Crm2Contract`

### Fluxos presentes
- gerar proposta
- salvar proposta
- gerar PDF
- enviar proposta
- aceitar/rejeitar proposta
- gerar contrato
- enviar contrato
- aceitar/rejeitar contrato
- criar cliente a partir do lead

Isso vai além de CRM e entra no processo comercial completo.

---

## 11. Financeiro PJ
Rotas principais:
- `/financeiro/dashboard`
- `/financeiro/contas`
- `/financeiro/centros-custo`
- `/financeiro/lancamentos`
- `/financeiro/relatorios`
- `/financeiro/metas`
- `/financeiro/fornecedores`

### O módulo cobre
- dashboard financeiro
- contas e cartões
- centros de custo
- lançamentos
- fornecedores
- metas de caixa
- relatórios

### Entidades principais
- `FinCostCenter`
- `FinAccount`
- `FinTransaction`
- `FinGoal`
- `FinSupplier`

### Funcionalidades observadas
- contas wallet e credit_card
- saldo atual
- limite de crédito
- dia de vencimento e fechamento
- receitas e despesas
- lançamentos realizados ou pendentes
- comprovante/anexo financeiro
- parcelamento
- fornecedor vinculado
- cliente vinculado em lançamentos
- metas financeiras
- dados agregados para dashboard e relatórios

### Objetivo do módulo
Trazer para dentro do mesmo sistema a visão financeira básica da operação PJ, sem depender de ferramenta externa para controle do dia a dia.

---

## 12. API do projeto e API do sistema
Rotas principais:
- `/admin/system-api-keys`
- `/api/system-api-keys`
- `/api/project/<project_id>/api-keys`
- blueprint `api_v1`

O sistema tem uma API relativamente madura para integrações.

### Tipos de chave
1. **Chaves de projeto**
   - escopo limitado a um projeto
2. **Chaves de sistema**
   - escopo global, apenas admin

### Recursos expostos
- projeto
- tarefas
- todos
- clientes
- projetos globais
- usuários
- CRM leads/contatos
- tarefas do sistema

### Segurança
- token via `Authorization: Bearer`
- ou `X-API-Key`
- hash das chaves
- scopes por permissão
- revogação e expiração
- proteção anti-IDOR para tarefas/todos fora do escopo do projeto

### Além da API v1
Dentro da aba de projeto existem recursos para:
- credenciais de API do projeto
- endpoints do projeto
- api keys do projeto

Ou seja, o sistema não só consome integrações: ele ajuda a **governar integração por projeto**.

---

## 13. GitHub
Rotas principais:
- `/projects/<id>/github_data`
- `/projects/<id>/github_commit/<sha>`
- `/projects/<id>/github_commits_list`
- `/projects/<id>/github_file_content`
- `/projects/<id>/github_file_commit`

### O que existe
- salvar repo GitHub no projeto
- consumir commits recentes
- ler arquivos do repo
- recuperar commit de arquivo
- usar token pessoal do usuário/admin com fallback
- usar commits como contexto para IA
- gerar to-dos a partir de commits

### Papel do GitHub no sistema
O GitHub não aparece como enfeite. Ele é parte do contexto técnico do projeto.

---

## 14. Arquivos
Rotas principais:
- `/api/project/<project_id>/files`
- `/project/<project_id>/files/<file_id>/download`
- `/project/<project_id>/files/<file_id>/preview`
- `/api/crm/contato/<contato_id>/files`

### O módulo suporta
- upload de arquivos por projeto
- categorias de arquivo
- preview
- download
- update/delete
- anexos de CRM
- uploads financeiros

### Tipos aceitos
O `app.py` mostra uma lista ampla, incluindo:
- PDF
- imagens
- Office
- ZIP/RAR
- CSV/TXT
- áudio/vídeo
- arquivos de design como Figma/Sketch/PSD/AI

Isso sugere uso operacional real para documentação técnica e comercial.

---

## 15. Relatórios
Rotas principais:
- `/reports`
- `/reports/generate_pdf`
- `/admin/export-data`
- `/admin/import-data`
- `/admin/export-tasks`
- `/admin/import-tasks`

### O módulo entrega
- relatórios por cliente/projeto/tarefa
- PDF
- export/import operacional
- extração de dados para continuidade e backup

É tanto camada de reporting quanto ferramenta de administração.

---

## 16. Monitoramento RPA
Arquivos relevantes:
- `rpa_monitor_client/`
- inicialização em `app.py`

### O que indica
O sistema também serve como central de automações, com:
- identificação de robô/app
- logs por região
- monitoramento em tempo real via websocket
- status de RPA no contexto dos projetos

Isso casa com o campo `rpa_identifier` em projetos e com os badges visuais no grid de projetos.

---

## 17. Botões e ações importantes que aparecem no produto

## Projetos
- Criar Novo Projeto
- Editar
- Excluir
- Nova Reunião
- Processar com IA
- Histórico
- Ver no Kanban
- Criar projeto vinculado
- Vincular projeto existente

## Tarefas
- Tarefa Manual
- Tarefa Simples
- Gerar com IA
- Editar
- Deletar
- Disparar

## Kanban
- Nova Tarefa
- Incluir Transcrição
- filtros por cliente/projeto
- drag-and-drop

## Reuniões
- Sincronizar Google
- Nova análise
- Criar nova reunião
- Gerar pauta
- Importar do calendário
- Sincronizar Fireflies
- Analisar reunião

## CRM2
- mover lead
- arquivar
- gerar pauta
- criar reunião
- gerar proposta
- enviar proposta
- aceitar/rejeitar proposta
- gerar contrato
- enviar contrato
- aceitar/rejeitar contrato
- criar cliente

## Financeiro
- cadastrar conta
- cadastrar centro de custo
- cadastrar fornecedor
- novo lançamento
- metas
- relatórios

---

## Modelos centrais de dados

Algumas entidades principais identificadas em `models.py`:
- `User`
- `Client`
- `Project`
- `ProjectStatusHistory`
- `Task`
- `TodoItem`
- `Contato`
- `Comentario`
- `CrmStage`
- `Crm2Lead`
- `Crm2Meeting`
- `Crm2Notification`
- `Crm2Proposal`
- `Crm2Contract`
- `ProjectFile`
- `ProjectApiCredential`
- `ProjectApiEndpoint`
- `ProjectApiKey`
- `SystemApiKey`
- `FinCostCenter`
- `FinAccount`
- `FinTransaction`
- `FinGoal`
- `FinSupplier`
- `Meeting`
- `UserIntegrationCredential`
- `AiChatHistory`

---

## Fluxo operacional resumido do sistema inteiro

### Fluxo comercial e entrega
1. lead entra no CRM/CRM2
2. equipe movimenta o lead no pipeline
3. reuniões são criadas ou sincronizadas
4. IA gera pauta e/ou analisa transcrição
5. lead pode receber proposta e contrato
6. lead vira cliente
7. cliente recebe projeto
8. projeto recebe escopo, equipe, datas, integrações e arquivos
9. tarefas e to-dos são gerados
10. execução acontece no Kanban
11. cliente pode acompanhar via acesso público
12. operação e gestão acompanham indicadores no dashboard

### Fluxo técnico
1. projeto recebe repo GitHub / drive / env / backup / SSH
2. GitHub alimenta contexto técnico
3. commits podem virar to-dos
4. API keys permitem integrações externas por projeto ou sistema
5. RPA monitor complementa o status operacional

### Fluxo de reuniões
1. reunião criada manualmente ou pelo Google
2. agenda gerada com IA
3. transcrição obtida manualmente ou via Fireflies
4. IA resume, estrutura ações e mede alinhamento
5. reunião alimenta projeto, lead ou execução

---

## Design e experiência

O `DESIGN.md` deixa claro que a intenção é um **centro de comando premium em dark mode**, com referências de:
- Linear
- Spotify
- Raycast

### Características do design
- camadas escuras com profundidade
- verde funcional como cor de ação
- alertas operacionais com prioridade visual
- cards premium
- glow pontual para estados críticos
- foco em operação, não marketing

Isso aparece especialmente em:
- dashboard
- cards de projeto
- kanban
- notificações
- painel de reuniões

---

## Restrições e pontos de atenção

- monólito grande, com muita lógica concentrada em `routes.py`
- migrações parcialmente distribuídas entre startup e scripts auxiliares
- dependência externa de OpenAI, Google, Fireflies, SMTP e GitHub
- upload em disco local
- sistema single-tenant / interno
- algumas partes mostram evolução incremental e coexistência de módulos antigos/novos (ex.: CRM e CRM2)

---

## Em uma frase

**FGinovaigestao é uma central operacional interna que conecta comercial, reuniões, projetos, tarefas, integrações técnicas, financeiro e API em um único sistema web orientado à execução.**
