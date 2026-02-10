### Descrição Resumida
O **Gestão Inovai** é uma plataforma web robusta de Gestão de Projetos e Tarefas desenvolvida em Python/Flask. O sistema atua como um hub centralizador para operações da empresa, integrando gestão clássica de projetos (Ciclo de Vida, Kanban, Prazos) com recursos avançados de Inteligência Artificial (OpenAI GPT-4o) para automação de escopo e tarefas a partir de transcrições de reuniões. Além disso, possui módulo dedicado para monitoramento em tempo real de robôs RPA (Robotic Process Automation).

### Problema/Oportunidade
A organização enfrentava a fragmentação de informações entre planilhas desconexas, falta de padronização na definição de escopos de projetos e dificuldade em monitorar a saúde dos robôs de automação (RPA) em uma única interface.
**Oportunidade:** Criar uma "Torre de Controle" unificada que não apenas gerencia o trabalho humano, mas também monitora a força de trabalho digital (RPA) e utiliza IA para reduzir drasticamente o tempo gasto na estruturação inicial de projetos (setup time).

### Objetivos
1.  **Centralização:** Unificar dados de Clientes, Projetos, Tarefas e Usuários em um único banco de dados relacional.
2.  **Automação Inteligente:** Utilizar IA Generativa para converter transcrições brutas de reuniões em escopos de projeto estruturados (Objetivos, Riscos, Premissas) e listas de tarefas acionáveis.
3.  **Gestão Visual:** Oferecer interface Kanban para acompanhamento intuitivo do fluxo de trabalho.
4.  **Monitoramento Híbrido:** Rastrear status de projetos de software e execuções de RPA no mesmo painel administrativo.
5.  **Padronização:** Forçar o preenchimento de metadados técnicos cruciais (Ex: "Possui .ENV?", "Possui Backup?") para garantir qualidade na entrega.

### Alinhamento Estratégico
A arquitetura monolítica modular em Flask permite desenvolvimento ágil e fácil manutenção, ideal para a escala atual da operação.
*   **IA-First:** A integração profunda com a OpenAI coloca a empresa na vanguarda da gestão aumentada, preparando o terreno para futuros agentes autônomos.
*   **RPA-Ready:** O módulo nativo de monitoramento de RPA alinha o software com a estratégia de hiperautomação da empresa.
*   **Escalabilidade:** O uso de SQLAlchemy e Gunicorn prepara o sistema para migração transparente de SQLite para PostgreSQL em ambientes de produção de alta demanda.

### Escopo do Projeto
O sistema atual implementa os seguintes módulos e funcionalidades:

*   **Autenticação e Controle de Acesso:** Login seguro, recuperação de senha via token/email, e controle de acesso baseado em papéis (Admin/User) e permissões granulares por módulo (Clientes, Projetos, CRM).
*   **Gestão de Projetos:** CRUD completo, indicadores visuais de estado (3-state toggles para requisitos técnicos), upload de arquivos, e associação de equipes.
*   **Módulo de IA:**
    *   Processamento de transcrições para geração de JSON estruturado (Escopo, Justificativa, Riscos).
    *   Geração automática de tarefas detalhadas "Sara Chen Persona" (PM Sênior) via GPT-4o.
*   **Gestão de Tarefas (Kanban):** Quadro visual com filtros, drag-and-drop (implícito na UI), e cálculo automático de progresso.
*   **Monitoramento RPA:** Cliente WebSocket integrado para receber status em tempo real de robôs remotos.
*   **Gestão de Clientes:** Cadastro unificado de clientes e empresas vinculadas.
*   **Dashboard:** Visão geral com KPIs, atividades recentes e atalhos rápidos.

### Fora do Escopo
*   **Faturamento Financeiro:** O sistema não processa pagamentos, emissão de notas fiscais ou controle de fluxo de caixa detalhado.
*   **Aplicativo Mobile Nativo:** A solução é exclusivamente Web Responsiva, sem apps nativos para iOS/Android no momento.
*   **Chat em Tempo Real:** Não há sistema de mensagens instantâneas entre usuários (apenas comentários/logs em tarefas).
*   **Multi-Tenancy:** O software foi desenhado para uso de uma única organização (Single Tenant), não operando como SaaS para múltiplas empresas isoladas.

### Premissas
*   **Tech Stack:** Backend em Python 3.12+ com Flask; Frontend em HTML5/Bootstrap 5 com Renderização no Servidor (Jinja2).
*   **Banco de Dados:** SQLite para desenvolvimento/homologação, pronto para PostgreSQL (via `psycopg2`).
*   **Infraestrutura:** Servidor Linux com Gunicorn como WSGI Server.
*   **Dependências Externas:** Acesso constante à internet requerido para APIs da OpenAI e serviços de E-mail (SMTP Gmail).

### Restrições
*   **Custo de Operação de IA:** O uso intensivo das funcionalidades de transcrição gera custos variáveis atrelados à API da OpenAI.
*   **Conectividade:** O monitoramento de RPA depende de conexão Websocket estável; falhas de rede podem gerar "falsos negativos" no status dos robôs.
*   **Performance de Upload:** O processamento de arquivos grandes (uploads) é limitado pela configuração do servidor e não utiliza armazenamento em nuvem distribuído (S3) na versão atual, salvando em disco local (`/uploads`).
