# Plano de Implementação Atômico: Organização Estruturada e Refatoração

**Status:** Planejado
**Data:** 09/02/2026
**Responsável:** Arquiteto de Software / Tech Lead

## 1. Contexto e Análise (Últimos 15 Dias)
A análise do histórico recente e da estrutura de arquivos revela um foco intenso em correções rápidas (Hotfixes) e ajustes de esquema de banco de dados, resultando no acúmulo de scripts de manutenção na raiz do projeto e um arquivo de rotas (`routes.py`) sobrecarregado.

### Diagnóstico Atual:
*   **Poluição da Raiz:** Existência de múltiplos scripts temporários (`fix_*.py`, `migrate_*.py`, `debug_*.py`) misturados ao código fonte principal.
*   **Monólito de Rotas:** O arquivo `routes.py` centraliza todas as lógicas (Projetos, Tarefas, Usuários, API), dificultando a manutenção e testes isolados.
*   **Ajustes Recentes (Concluídos):**
    *   [x] Implementação de Toggles de 3 Estados (.ENV/Backup).
    *   [x] Correção de perda de dados na edição rápida.
    *   [x] Documentação Técnica Inicial.

---

## 2. Plano de Ação (Checklist)

### 2.1. Organização e Limpeza (Housekeeping)
O objetivo é limpar a raiz do projeto para manter apenas arquivos de configuração e entrypoints.

- [ ] **Auditoria de Scripts**
    - [ ] Criar diretório `scripts/maintenance` para scripts de migração e correção (`fix_bool_data.py`, `migrate_bools.py`).
    - [ ] Criar diretório `scripts/debug` para scripts de diagnóstico (`debug_regex.py`, `check_schema.py`).
    - [ ] Mover arquivos correspondentes para os novos diretórios.
    - [ ] Remover scripts obsoletos ou duplicados (ex: `fix_routes_v2.py` vs `fix_routes_final_v2.py`).

### 2.2. Backend (Refatoração Estrutural)
O objetivo é modularizar o `routes.py` utilizando *Blueprints* do Flask.

- [ ] **Configuração de Blueprints**
    - [ ] Criar pacote `routes/` (com `__init__.py`).
    - [ ] Criar `routes/projects.py` e mover rotas relacionadas a projetos (`/projects`, `/project/<id>`).
    - [ ] Criar `routes/tasks.py` e mover rotas de tarefas e kanban.
    - [ ] Criar `routes/api.py` para endpoints JSON.
    - [ ] Criar `routes/auth.py` para Login/Logout e gestão de usuários.
    - [ ] Atualizar `app.py` para registrar os novos Blueprints.

### 2.3. Frontend (Manutenção e Padronização)
Garantir que as alterações de backend não quebrem os templates.

- [ ] **Verificação de Referências**
    - [ ] Verificar chamadas `url_for` nos templates (`projects.html`, `kanban.html`) para garantir compatibilidade com novos endpoints (caso nomes mudem, manter compatibilidade).
    - [ ] Centralizar assets estáticos se necessário.

### 2.4. Verificação e Qualidade
- [ ] **Testes de Regressão**
    - [ ] Verificar login e logout.
    - [ ] Testar CRUD de projetos (criação, edição 3-estados, exclusão).
    - [ ] Testar movimentação de cards no Kanban.
- [ ] **Validação de Deploy**
    - [ ] Garantir que o `gunicorn` continue apontando para o `app:app` corretamente após refatoração.

---

## 3. Arquivos Envolvidos
*   `routes.py` (Decomposição)
*   `app.py` (Registro de Blueprints)
*   `scripts/` (Novo diretório)
*   `templates/*.html` (Revisão de links)

## 4. Próximos Passos
Aprovação deste plano para início imediato da Fase 2.1 (Organização).
