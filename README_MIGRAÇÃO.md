# 🚀 Guia de Migração de Dados - Desenvolvimento → Produção

## Como usar os scripts de migração

### 📤 PASSO 1: Exportar dados do Desenvolvimento

No **ambiente de desenvolvimento**, execute:

```bash
python3 export_data.py
```

Isso vai criar um arquivo `database_export_YYYYMMDD_HHMMSS.json` com todos os seus dados.

### 📁 PASSO 2: Transferir o arquivo para Produção

Copie o arquivo JSON gerado para o ambiente de produção.

### 📥 PASSO 3: Importar dados na Produção

No **ambiente de produção**, execute:

```bash
# Usar o arquivo mais recente automaticamente
python3 import_data.py

# OU especificar um arquivo específico
python3 import_data.py database_export_20250826_231327.json
```

## ⚠️ IMPORTANTES

1. **Execute no ambiente correto**:
   - `export_data.py` = desenvolvimento
   - `import_data.py` = produção

2. **Dados existentes**: O script não duplica dados. Se um usuário/cliente já existir (mesmo email/nome), ele será pulado.

3. **Senhas**: Todas as senhas são mantidas como estavam no desenvolvimento.

4. **Códigos públicos**: Os códigos de acesso dos clientes são preservados.

## 📊 O que é migrado

- ✅ **Usuários** (6 usuários com senhas)
- ✅ **Clientes** (4 clientes com códigos públicos)  
- ✅ **Projetos** (14 projetos completos com IA)
- ✅ **Tarefas** (92 tarefas organizadas)
- ✅ **ToDos** (5 itens de sub-tarefas)

## 🔑 Credenciais após migração

- **Admin**: admin@sistema.com / admin123
- **Outros**: [email] / senha original

**⚠️ ALTERE AS SENHAS APÓS O PRIMEIRO LOGIN!**