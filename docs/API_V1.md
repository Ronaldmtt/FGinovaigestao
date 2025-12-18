# API v1 - Documentação

Esta API permite integrar sistemas externos com o sistema de gestão de projetos. Existem dois tipos de chaves de API:

1. **Chaves de Projeto**: Vinculadas a um projeto específico
2. **Chaves de Sistema**: Acesso geral a todos os dados (apenas admin)

## Resumo das Mudanças Recentes

| Commit | Descrição |
|--------|-----------|
| API Geral | Novos endpoints para clientes, projetos, tarefas e usuários com acesso global |
| Chaves de Sistema | Administradores podem criar chaves com acesso a todo o sistema |
| Formatação JSON | Respostas da API formatadas com indentação |
| Validação de usuários | Tarefas só podem ser atribuídas a membros do projeto (proteção anti-IDOR) |

---

## Autenticação

A API usa autenticação via chave de API (API Key). Você pode enviar a chave de duas formas:

### Opção 1: Header Authorization (Recomendado)
```bash
curl -H "Authorization: Bearer SUA_CHAVE_AQUI" https://seu-dominio.com/api/v1/project
```

### Opção 2: Header X-API-Key
```bash
curl -H "X-API-Key: SUA_CHAVE_AQUI" https://seu-dominio.com/api/v1/project
```

---

## Tipos de Chaves de API

### Chaves de Projeto (Project API Key)
- Vinculadas a um projeto específico
- Criadas na aba "API" de cada projeto
- Acesso restrito ao projeto da chave

### Chaves de Sistema (System API Key)
- Acesso geral a todo o sistema
- Criadas apenas por administradores
- Menu: **API do Sistema** (barra lateral)
- Permitem acesso a clientes, todos os projetos, todas as tarefas e usuários

---

## Como Obter uma Chave de API

### Chave de Projeto
1. Acesse o projeto no sistema
2. Clique na aba **"API"**
3. Clique em **"Gerar Nova Chave"**
4. Configure nome, permissões e validade
5. **IMPORTANTE**: Copie a chave imediatamente!

### Chave de Sistema (Admin)
1. No menu lateral, clique em **"API do Sistema"**
2. Clique em **"Nova Chave"**
3. Configure nome, permissões e validade
4. **IMPORTANTE**: Copie a chave imediatamente!

---

## Permissões Disponíveis (Scopes)

### Chaves de Projeto
| Scope | Descrição |
|-------|-----------|
| `projects:read` | Ler informações do projeto |
| `tasks:read` | Listar e visualizar tarefas |
| `tasks:write` | Criar, editar e excluir tarefas |

### Chaves de Sistema
| Scope | Descrição |
|-------|-----------|
| `clients:read` | Listar e visualizar clientes |
| `clients:write` | Criar, editar e excluir clientes |
| `projects:read` | Listar e visualizar todos os projetos |
| `projects:write` | Criar, editar e excluir projetos |
| `tasks:read` | Listar e visualizar todas as tarefas |
| `tasks:write` | Criar, editar e excluir tarefas |
| `users:read` | Listar e visualizar usuários |

---

## Endpoints Disponíveis

### Base URL
```
https://seu-dominio.com/api/v1
```

---

## 1. Projeto

### GET /api/v1/project
Retorna informações do projeto vinculado à chave de API.

**Permissão necessária:** `projects:read`

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE" https://seu-dominio.com/api/v1/project
```

**Resposta:**
```json
{
  "success": true,
  "project": {
    "id": 42,
    "nome": "Sistema de Gestão",
    "descricao_resumida": "Plataforma web para gestão de tarefas",
    "objetivos": "Otimizar a organização de equipes",
    "status": "em_andamento",
    "prazo": "2025-12-31",
    "progress_percent": 45,
    "responsible": {
      "id": 5,
      "nome": "João Silva"
    },
    "client": {
      "id": 2,
      "nome": "Empresa ABC"
    },
    "created_at": "2025-01-15T10:30:00"
  }
}
```

---

## 2. Tarefas

### GET /api/v1/tasks
Lista todas as tarefas do projeto.

**Permissão necessária:** `tasks:read`

**Parâmetros de query (opcionais):**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `status` | string | Filtrar por status: `pendente`, `em_andamento`, `concluida` |
| `assigned_user_id` | integer | Filtrar por usuário responsável |

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE" "https://seu-dominio.com/api/v1/tasks?status=pendente"
```

**Resposta:**
```json
{
  "success": true,
  "tasks": [
    {
      "id": 101,
      "titulo": "Criar tela de login",
      "descricao": "Desenvolver interface de autenticação",
      "status": "pendente",
      "prioridade": "alta",
      "data_conclusao": "2025-02-01",
      "assigned_user": {
        "id": 5,
        "nome": "João Silva"
      },
      "todos_count": 3,
      "todos_completed": 1,
      "created_at": "2025-01-20T14:00:00"
    }
  ],
  "total": 1
}
```

---

### GET /api/v1/tasks/{task_id}
Retorna detalhes de uma tarefa específica.

**Permissão necessária:** `tasks:read`

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE" https://seu-dominio.com/api/v1/tasks/101
```

---

### POST /api/v1/tasks
Cria uma nova tarefa.

**Permissão necessária:** `tasks:write`

**Body (JSON):**
```json
{
  "titulo": "Nova funcionalidade",
  "descricao": "Descrição detalhada da tarefa",
  "status": "pendente",
  "prioridade": "media",
  "data_conclusao": "2025-03-01",
  "assigned_user_id": 5
}
```

**Campos obrigatórios:** `titulo`

**Campos opcionais:**
| Campo | Tipo | Valores válidos |
|-------|------|-----------------|
| `descricao` | string | Texto livre |
| `status` | string | `pendente`, `em_andamento`, `concluida` |
| `prioridade` | string | `baixa`, `media`, `alta` |
| `data_conclusao` | string | Data no formato ISO (YYYY-MM-DD) |
| `assigned_user_id` | integer | ID de um membro do projeto |

**Exemplo:**
```bash
curl -X POST \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Implementar relatórios", "prioridade": "alta"}' \
  https://seu-dominio.com/api/v1/tasks
```

---

### PUT /api/v1/tasks/{task_id}
Atualiza uma tarefa existente.

**Permissão necessária:** `tasks:write`

**Body (JSON):** Mesmos campos do POST (todos opcionais)

**Exemplo:**
```bash
curl -X PUT \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"status": "em_andamento"}' \
  https://seu-dominio.com/api/v1/tasks/101
```

---

### DELETE /api/v1/tasks/{task_id}
Remove uma tarefa.

**Permissão necessária:** `tasks:write`

**Exemplo:**
```bash
curl -X DELETE \
  -H "Authorization: Bearer SUA_CHAVE" \
  https://seu-dominio.com/api/v1/tasks/101
```

---

## 3. Subtarefas (Todos)

### GET /api/v1/tasks/{task_id}/todos
Lista subtarefas de uma tarefa.

**Permissão necessária:** `tasks:read`

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE" https://seu-dominio.com/api/v1/tasks/101/todos
```

**Resposta:**
```json
{
  "success": true,
  "todos": [
    {
      "id": 501,
      "titulo": "Criar mockup",
      "descricao": "Design inicial da tela",
      "concluida": true,
      "ordem": 1,
      "assigned_user": {
        "id": 5,
        "nome": "João Silva"
      }
    }
  ],
  "total": 1
}
```

---

### POST /api/v1/tasks/{task_id}/todos
Cria uma nova subtarefa.

**Permissão necessária:** `tasks:write`

**Body (JSON):**
```json
{
  "titulo": "Revisar código",
  "descricao": "Code review da implementação",
  "assigned_user_id": 5
}
```

---

### PUT /api/v1/todos/{todo_id}
Atualiza uma subtarefa.

**Permissão necessária:** `tasks:write`

**Exemplo - Marcar como concluída:**
```bash
curl -X PUT \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"concluida": true}' \
  https://seu-dominio.com/api/v1/todos/501
```

---

### DELETE /api/v1/todos/{todo_id}
Remove uma subtarefa.

**Permissão necessária:** `tasks:write`

---

# API GERAL DO SISTEMA (Chaves de Sistema)

Os endpoints abaixo requerem uma **Chave de Sistema** (System API Key), criada por administradores no menu "API do Sistema".

---

## 4. Clientes

### GET /api/v1/clients
Lista todos os clientes.

**Permissão necessária:** `clients:read`

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE_SISTEMA" https://seu-dominio.com/api/v1/clients
```

**Resposta:**
```json
{
  "success": true,
  "clients": [
    {
      "id": 1,
      "nome": "Empresa ABC",
      "email": "contato@empresa.com",
      "telefone": "(11) 99999-9999",
      "empresa": "ABC Ltda",
      "projects_count": 5
    }
  ],
  "total": 1
}
```

---

### GET /api/v1/clients/{id}
Retorna detalhes de um cliente específico.

**Permissão necessária:** `clients:read`

---

### POST /api/v1/clients
Cria um novo cliente.

**Permissão necessária:** `clients:write`

**Body (JSON):**
```json
{
  "nome": "Novo Cliente",
  "email": "cliente@empresa.com",
  "telefone": "(11) 98888-8888",
  "empresa": "Empresa XYZ"
}
```

---

### PUT /api/v1/clients/{id}
Atualiza um cliente.

**Permissão necessária:** `clients:write`

---

### DELETE /api/v1/clients/{id}
Remove um cliente (apenas se não tiver projetos vinculados).

**Permissão necessária:** `clients:write`

---

## 5. Projetos (Geral)

### GET /api/v1/projects
Lista todos os projetos do sistema.

**Permissão necessária:** `projects:read`

**Parâmetros de query (opcionais):**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `status` | string | Filtrar por status |
| `client_id` | integer | Filtrar por cliente |

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE_SISTEMA" "https://seu-dominio.com/api/v1/projects?status=em_andamento"
```

---

### GET /api/v1/projects/{id}
Retorna detalhes completos de um projeto.

**Permissão necessária:** `projects:read`

---

### POST /api/v1/projects
Cria um novo projeto.

**Permissão necessária:** `projects:write`

**Body (JSON):**
```json
{
  "nome": "Novo Projeto",
  "client_id": 1,
  "responsible_id": 5,
  "status": "em_andamento",
  "prazo": "2025-12-31",
  "descricao_resumida": "Descrição do projeto"
}
```

**Campos obrigatórios:** `nome`, `client_id`

---

### PUT /api/v1/projects/{id}
Atualiza um projeto.

**Permissão necessária:** `projects:write`

---

### DELETE /api/v1/projects/{id}
Remove um projeto.

**Permissão necessária:** `projects:write`

---

## 6. Tarefas (Geral)

### GET /api/v1/system/tasks
Lista todas as tarefas do sistema (sem filtro de projeto).

**Permissão necessária:** `tasks:read`

**Parâmetros de query (opcionais):**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `status` | string | Filtrar por status |
| `project_id` | integer | Filtrar por projeto |
| `assigned_user_id` | integer | Filtrar por responsável |

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE_SISTEMA" "https://seu-dominio.com/api/v1/system/tasks?status=pendente"
```

---

### POST /api/v1/system/tasks
Cria uma tarefa em qualquer projeto.

**Permissão necessária:** `tasks:write`

**Body (JSON):**
```json
{
  "titulo": "Nova tarefa via API",
  "project_id": 42,
  "descricao": "Descrição da tarefa",
  "status": "pendente",
  "prioridade": "alta",
  "assigned_user_id": 5
}
```

**Campos obrigatórios:** `titulo`, `project_id`

---

## 7. Usuários

### GET /api/v1/users
Lista todos os usuários do sistema.

**Permissão necessária:** `users:read`

**Exemplo:**
```bash
curl -H "Authorization: Bearer SUA_CHAVE_SISTEMA" https://seu-dominio.com/api/v1/users
```

**Resposta:**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "nome": "João",
      "sobrenome": "Silva",
      "email": "joao@empresa.com",
      "is_admin": false
    }
  ],
  "total": 1
}
```

---

### GET /api/v1/users/{id}
Retorna detalhes de um usuário.

**Permissão necessária:** `users:read`

---

## Códigos de Erro

| Código HTTP | Erro | Descrição |
|-------------|------|-----------|
| 401 | `missing_api_key` | Chave de API não fornecida |
| 401 | `invalid_api_key` | Chave inválida, expirada ou revogada |
| 403 | `insufficient_scope` | Chave não tem permissão para esta operação |
| 400 | `missing_field` | Campo obrigatório não informado |
| 400 | `invalid_user` | Usuário não faz parte do projeto |
| 404 | `not_found` | Recurso não encontrado |

**Formato de erro:**
```json
{
  "success": false,
  "error": {
    "code": "invalid_api_key",
    "message": "Chave de API inválida ou expirada"
  }
}
```

---

## Exemplos Práticos

### Fluxo completo: Criar tarefa com subtarefas

```bash
# 1. Criar tarefa
curl -X POST \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Desenvolver módulo de pagamentos", "prioridade": "alta"}' \
  https://seu-dominio.com/api/v1/tasks

# Resposta: {"success": true, "task": {"id": 102, ...}}

# 2. Adicionar subtarefas
curl -X POST \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Integrar gateway de pagamento"}' \
  https://seu-dominio.com/api/v1/tasks/102/todos

curl -X POST \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Implementar webhooks"}' \
  https://seu-dominio.com/api/v1/tasks/102/todos

# 3. Marcar subtarefa como concluída
curl -X PUT \
  -H "Authorization: Bearer SUA_CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"concluida": true}' \
  https://seu-dominio.com/api/v1/todos/503
```

### Listar tarefas pendentes de um usuário

```bash
curl -H "Authorization: Bearer SUA_CHAVE" \
  "https://seu-dominio.com/api/v1/tasks?status=pendente&assigned_user_id=5"
```

---

## Segurança

- **Nunca compartilhe sua chave de API** em código público ou repositórios
- As chaves são armazenadas com hash SHA-256 (não podem ser recuperadas)
- Configure a menor permissão necessária para cada integração
- Defina data de expiração para chaves temporárias
- Revogue chaves que não são mais necessárias

---

## Limites

- Máximo de 100 requisições por minuto por chave
- Payload máximo: 1MB por requisição
- Chaves expiradas são automaticamente invalidadas
