# 💰 Financeiro InovaiLab

> **Controle financeiro inteligente para pessoas físicas e jurídicas**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Sobre o Projeto

O **Financeiro InovaiLab** é uma aplicação web mobile-first para controle de finanças pessoais e empresariais. A dor que resolve é simples: a maioria das pessoas **não sabe para onde vai seu dinheiro** — e quando percebe, já é tarde demais para agir.

Com o Financeiro InovaiLab, você lança gastos manualmente em segundos, classifica por centros de custo personalizados e acompanha tudo em um dashboard visual rico com gráficos interativos.

---

## 🌟 Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 🔐 Autenticação | Cadastro e login por e-mail/senha |
| 👤 / 🏢 Tipos de conta | Pessoa Física ou Jurídica |
| 🏷️ Centros de custo | Categorias customizáveis (editar, adicionar, remover) |
| 👜 Carteiras | Contas manuais com controle de saldo |
| 💳 Cartões de crédito | Controle de fatura, limite e vencimento |
| 💸 Lançamentos manuais | Registre despesas e receitas em segundos |
| 📊 Dashboard | Saldo atual, receitas, despesas, balanço do mês |
| 📈 Relatórios | Gráficos por categoria, tendência mensal, projeção anual |
| 🎯 Metas financeiras | Defina, acompanhe e deposite em metas de economia |
| 📱 Mobile-first | Interface otimizada para celular (Android e iOS via browser) |

---

## 🏗️ Arquitetura

```
Flask (Backend API + SSR Templates)
├── Auth Blueprint       → /auth/*
├── Onboarding Blueprint → /onboarding/*
├── Accounts Blueprint   → /api/accounts/*
├── Transactions API     → /api/transactions/*
├── Dashboard API        → /api/dashboard/*
├── Goals API            → /api/goals/*
└── Main Blueprint       → / (dashboard pages)

PostgreSQL (banco de dados)
└── users, cost_centers, accounts, transactions, goals

Frontend
├── HTML/CSS/JS (mobile-first dark theme)
└── Chart.js (gráficos do dashboard de relatórios)
```

---

## 🚀 Setup Local (Desenvolvimento)

### Pré-requisitos
- Python 3.11+
- PostgreSQL 14+ rodando localmente
- Git

### 1. Clonar o repositório
```bash
git clone https://github.com/inovailab/ronald-Financeiro-Inovailab.git
cd ronald-Financeiro-Inovailab
```

### 2. Criar e ativar o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
```bash
# Copie o .env.example e ajuste os valores
cp .env.example .env
```

Edite o `.env`:
```env
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://postgres:sua-senha@localhost:5432/financeiro_inovailab
```

### 5. Criar o banco de dados
```bash
# Crie o banco no PostgreSQL
psql -U postgres -c "CREATE DATABASE financeiro_inovailab;"

# Rodar migrações
flask db init
flask db migrate -m "initial"
flask db upgrade
```

### 6. Iniciar o servidor
```bash
python run.py
```

✅ Acesse: `http://localhost:5000` (use DevTools → toggle mobile viewport para simular celular)

---

## 🚢 Deploy na GCP (Produção)

### Stack de Produção
- **Gunicorn** (WSGI server)
- **Nginx** (reverse proxy)
- **PostgreSQL** (local na VM)
- **Systemd** (gerenciamento do processo)

### Deploy rápido
```bash
# Na VM do Google Cloud:
git pull origin main
sudo systemctl restart financeiro
```

### Configuração do serviço Systemd
```bash
# Copie o arquivo systemd incluído no repositório
sudo cp financeiro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable financeiro
sudo systemctl start financeiro
```

### Nginx config básico
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://unix:/tmp/financeiro.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📱 App Mobile

O Financeiro InovaiLab é uma **PWA (Progressive Web App)** — funciona em qualquer celular moderno sem necessidade de publicação em app stores:

- **Android**: Abra no Chrome → "Adicionar à tela inicial"
- **iOS**: Abra no Safari → Compartilhar → "Adicionar à tela de início"

---

## 🔄 Fluxo de Atualização

```
Desenvolvimento local
      ↓
git add . && git commit -m "feat: descrição"
      ↓
git push origin main
      ↓
Na VM GCP: git pull && sudo systemctl restart financeiro
```

---

## 📋 Fluxo do Usuário

```
1. Cadastro (e-mail + senha)
2. Escolha: Pessoa Física ou Jurídica
3. Configurar centros de custo (sugestões personalizáveis)
4. Adicionar conta (carteira ou cartão de crédito)
5. Dashboard pronto!
   ├── Lançar gastos manualmente
   ├── Ver saldo por conta
   ├── Analisar gráficos no relatório
   └── Acompanhar metas de economia
```

---

## 🛣️ Roadmap

- [x] MVP — Autenticação, contas, cartões, lançamentos, dashboard, metas
- [ ] Login com Google (OAuth 2.0)
- [ ] Notificações de vencimento de fatura
- [ ] Exportação de relatórios (PDF/CSV)
- [ ] App nativo (React Native / Flutter)
- [ ] Integração Open Finance

---

## 🤝 Desenvolvido por

**InovaiLab** — Soluções de tecnologia para negócios inteligentes.
