# Plano de Implementação Atômico — CRM 2 (FG Inovai Gestão)

> Gerado em: **12/02/2026** | Análise baseada no histórico de commits do dia e estado atual dos arquivos.

---

## Commits realizados HOJE (12/02/2026)

- [x] Implementar extração de To-Dos (DD/MM/YYYY) e análise com formatação na `lead_detail` [12/02/2026]
- [x] Implementar CRM 2 completo: sidebar, rotas, templates (leads, pipeline, lead_detail, notifications) [12/02/2026]
- [x] Feature: toggle de 3 estados para produtos no relatório [12/02/2026]
- [x] Fix: correção do toggle de 3 estados e prevenção de perda de dados [12/02/2026]
- [x] Fix: correção do comportamento visual do toggle de 3 estados [12/02/2026]
- [x] Feature: geração de relatórios PDF com contagens legíveis por humano [12/02/2026]
- [x] Feature: mover Notificações para aba top-level do sidebar com badge de contagem [12/02/2026]
- [x] Feature: botão de lixeira no pipeline para arquivar lead sem deletar do sistema [12/02/2026]

---

## Bugs Identificados

- [ ] **Bug Crítico — Criação de Reunião retorna 404**: O arquivo `static/js/crm2_lead_detail.js` (função `createMeeting`, linha 25) chama a URL `/api/crm2/lead/{id}/meeting`, porém a rota registrada em `routes.py` (linha 4620) é `/api/crm2/lead/{id}/reuniao`. Isso causa um erro `404 NOT FOUND` ao tentar criar uma reunião a partir da página de detalhes do lead. [12/02/2026]

---

## Tarefas Pendentes

- [ ] **Fix Backend/Frontend**: Corrigir a URL no arquivo `static/js/crm2_lead_detail.js` — alterar `/api/crm2/lead/${LEAD_ID}/meeting` para `/api/crm2/lead/${LEAD_ID}/reuniao` na função `createMeeting()` (linha 25). [12/02/2026]
- [ ] **Verificação**: Após o fix, testar a criação de reunião na página de detalhes de um lead e confirmar que o status retornado é `200 OK` (sem 404). [12/02/2026]
- [ ] **Verificação**: Confirmar que o lead avança automaticamente de estágio após a criação da reunião (comportamento esperado da rota `crm2_create_meeting`). [12/02/2026]
- [ ] **Deploy**: Executar `git pull && sudo systemctl restart gestao_app` no servidor de produção para aplicar todas as correções do dia. [12/02/2026]
- [ ] **Verificação Prod**: Testar no ambiente de produção: criação de lead, movimentação no pipeline, arquivamento via botão de lixeira, criação de reunião e badge de notificações no sidebar. [12/02/2026]

---

## Itens já concluídos e validados localmente

- [x] **Sidebar**: Notificações movidas de submenu do CRM 2 para item top-level com badge de contagem (vermelho, `bg-danger`). JS de polling atualizado para usar novo ID `notifCountBadge`. [12/02/2026]
- [x] **Pipeline**: Botão de lixeira adicionado em cada card do pipeline. Ao clicar, o lead é movido para estágio "Arquivado" (removido visualmente com animação) sem ser deletado do banco de dados. Rota `/api/crm2/archive` criada em `routes.py`. [12/02/2026]
- [x] **Templates**: Serialização de `Crm2Lead` corrigida em `leads.html` (linha 215) — `tojson` substituído por dicionário inline. [12/02/2026]
- [x] **Banco de Dados**: Colunas faltantes adicionadas via `ALTER TABLE` (`acesso_crm`, `acesso_clientes`, `acesso_projetos`, `acesso_tarefas`, `acesso_kanban`, `email_cliente`, `observacoes`). Tabela `crm2_contracts` criada. [12/02/2026]
- [x] **Relatórios**: Toggle de 3 estados (Ativo / Inativo / Todos) implementado e corrigido para contagens de produtos. Geração de PDF com contagens legíveis implementada. [12/02/2026]
