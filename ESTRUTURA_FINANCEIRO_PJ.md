# Guia de Estrutura: Módulo Financeiro para Gestão Empresarial (PJ)

Este documento detalha como adaptar a estrutura do projeto **Financeiro-Inova** (que originalmente é *mobile-first* e atende PF/PJ) para um **Módulo Financeiro Web** focado exclusivamente em **Pessoas Jurídicas (Empresas)**, desenhado para funcionar em desktops com uma **Barra Lateral (Sidebar)**.

---

## 1. Visão Geral da Interface (Layout Web / Desktop)

Como o sistema agora foca no uso corporativo pelo navegador desktop, a interface abandona as *bottom navigations* e *cards apertados* de mobile para dar lugar a um painel espaçoso.

A tela será dividida em:
- **Sidebar (Esquerda):** Menus gerais do ERP/Sistema. Dentro do menu principal haverá um grande bloco chamado **"Financeiro"**.
- **Área Principal (Workarea):** Onde o conteúdo das subabas será renderizado.

### Estrutura do Menu "Financeiro" na Sidebar:
* 📊 Dashboard
* 🗂️ Centros de Custo
* 🏦 Carteiras (Contas Bancárias/Caixa)
* 💳 Cartões de Crédito Corporativos
* 💸 Lançamentos
* 📈 Relatórios
* 🎯 Metas Financeiras

---

## 2. Estrutura do Banco de Dados (Modelagem Focada em PJ)

A grande diferença na modelagem para uso exclusivo de empresas é que os vínculos de dados não são necessariamente ligados ao `User` individual, mas sim à **Empresa (`company_id` ou `tenant_id`)**. 

> **O que eu pensei:** Ao focar só em CNPJ, você garante que qualquer sócio/funcionário com acesso àquela empresa veja o mesmo financeiro. Evitamos a complexidade de misturar PF e PJ.

**Tabelas Essenciais (Relacionamentos):**

1. **Empresa (Company)**: Representa o CNPJ. Todas as tabelas financeiras devem apontar para a `company_id`.
2. **Centro de Custo (CostCenter)**: Categorias das movimentações (Ex: "Marketing", "Folha de Pagamento", "Impostos").
3. **Conta (Account)**: Representa onde o dinheiro está fisicamente ou o meio de pagamento. Terá tipo: `wallet` (Conta Corrente/Caixa) ou `credit_card` (Cartão Corporativo).
4. **Transação (Transaction)**: Cada entrada ou saída. Aponta obrigatoriamente para uma `Account` e opcionalmente para um `CostCenter`.
5. **Metas (Goal)**: Objetivos de caixa (Ex: "Fundo de Reserva InovaiLab").

---

## 3. Detalhamento e Lógicas das Subabas

Abaixo, detalho **funcionalidade a funcionalidade** como você deve recriar no front-end e no back-end corporativo, o que foi pensado ao construir essa modelagem, e as lógicas de negócio cruciais.

### 3.1. 📊 Dashboard
**O que é**: O "Raio-X" das finanças da empresa. A primeira tela que o CFO ou Gestor vai ver.
**Elementos UI:**
- **Cards de Resumo (Topo):**
  - **Saldo Atual:** Soma do saldo de todas as `Accounts` do tipo `wallet`. *(Não soma cartão de crédito!)*
  - **Receitas do Mês:** Soma de `Transactions` de tipo `income` do mês vigente.
  - **Despesas do Mês:** Soma de `Transactions` de tipo `expense` do mês vigente.
  - **Balanço (Lucro/Prejuízo):** Receitas menos Despesas do mês.
- **Últimos Lançamentos (Tabela rápida):** Uma visão tabular das 5 ou 10 últimas movimentações.
**Dica de Implementação:** No backend, as consultas do Dashboard devem ser agrupadas e cacheadas se possível. Extraia o mês/ano direto no banco SQL para retornar só o total, em vez de carregar todas as transações na memória.

### 3.2. 🗂️ Centros de Custo (Categorias)
**O que é**: A organização do plano de contas gerencial da empresa.
**Elementos UI:**
- Tabela listando os centros de custo (Nome, Ícone, Cor, Status Ativo/Inativo).
- Botões para Editar, Adicionar e Remover.
**O que eu pensei:** Permitir customização de ícone e cor ajuda muito os relatórios (gráficos) a ficarem bonitos visualmente e fáceis de assimilar.
**Regra de Negócio Crucial:** Evite "deletar" um centro de custo (Hard Delete). Adicione um campo `is_active=False` (Soft Delete). Se tentar deletar uma categoria que já tem lançamentos lançados nela, haveria quebra de integridade ou dados orfãos. Apenas oculte-a em preenchimentos futuros.

### 3.3. 🏦 Carteiras (Contas Bancárias / Caixa)
**O que é**: As contas bancárias da empresa (Conta Banco do Brasil, Itaú, Conta Caixinha do Escritório).
**Elementos UI:**
- Lista em formato de Grid ou Tabela com os saldos individuais.
**O que eu pensei:** O saldo da `wallet` (`balance`) pode ser atualizado dinamicamente toda vez que um novo lançamento associado a ela é criado, editado ou removido.
**Aba de Transferências (Bônus):** É comum em empresas transferir dinheiro de uma conta para outra (ex: Caixa para o Banco). Isso gera duas transações: uma despesa na carteira A e uma receita na carteira B.

### 3.4. 💳 Cartões de Crédito Corporativos
**O que é**: Controle separado de despesas lançadas no limite de crédito da empresa.
**Elementos UI:**
- Visual de um "Cartão" desenhado em CSS.
- Progresso circular indicando limite consumido vs. e limite disponível.
- Dia do fechamento da fatura e data de vencimento.
**O que eu pensei e Como Calcular a Fatura:**
Um cartão **NÃO** tem um campo simples de "saldo a pagar" solto. O valor da fatura atual (`current_invoice`) é sempre a soma das transações de `expense` vinculadas àquela conta de cartão de crédito no **mês em vigência**.
A lógica computada fica assim:
`available_limit = credit_limit - current_invoice_sum`
> **Atenção:** Quando a fatura é paga, isso geralmente é feito saindo dinheiro de uma `wallet` para zerar o saldo negativo do cartão.

### 3.5. 💸 Lançamentos Manuais
**O que é**: Onde o dinheiro entra e sai. Tela central da operação.
**Elementos UI:**
- Tabela de dados ampla (Data, Conta, Categoria, Descrição, Valor, Botões de Ação).
- **Filtros avançados no topo:** Filtro por período, filtro por conta, filtro por categoria, pesquisa de texto pela descrição.
- Um botão grande "+ Novo Lançamento" que abre um formulário em Modal corporativo ou Side-panel (Drawer).
**O formulário precisa:**
- `Type` (Receita ou Despesa) (Radio buttons verde e vermelho ajudam o usuário)
- `Amount` (Campo com máscara monetária limpa). Transações saem como float no banco. Guarde as despesas como valores positivos no banco e gerencie no momento do cálculo, **ou** grave direto negativo. (O Financeiro-Inova gerencia pelo tipo e soma/subtrai onde precisa).
- `Cost Center` (Dropdown).
- `Account` (Dropdown).
- `Date` (Calendário).

### 3.6. 📈 Relatórios
**O que é**: Os "gráficos bonitos" para fechar reunião de diretoria.
**Elementos UI:**
- **Gráfico de Rosca/Pizza:** Repartindo os gastos no mês atual pelos `CostCenters` (usando as cores customizadas cadastradas pelo usuário).
- **Gráfico de Linha/Tendência (Tendência Mensal):** Eixo X são os meses (Jan, Fev, Mar...), Eixo Y tem duas linhas: Receitas (Verde) e Despesas (Vermelho).
- Use uma biblioteca poderosa e responsiva para web corporativa, como o **Chart.js** ou **ApexCharts**.
**O que eu pensei:** Esta aba traz o "Aha! moment". Retorne do backend o dado mastigado via um endpoint `/api/reports/` que já traz os arrays prontos para alimentar o ApexCharts, sem exigir cálculos pesados no front-end Vue/React/Angular.

### 3.7. 🎯 Metas Financeiras
**O que é**: Planejamento de capital de giro ou provisão (Ex: "Comprar equipamento X", "Décimo Terceiro").
**Elementos UI:**
- Cards com barra de progresso horizontal: `(current_amount / target_amount) * 100`.
- Botões: "Depositar na meta".
**O que eu pensei:** Muitas vezes, esse saldo sai temporariamente do visual do Dashboard regular para que os gestores percebam que aquele dinheiro está bloqueado para o propósito específico, ajudando no controle do fluxo de caixa e evitando que gastem capital de reserva.

---

## 4. Roteiro Passo a Passo de Implementação (Tutorial)

Caso você vá adaptar isso ativamente dentro de um sistema existente:

1. **Back-end e Migrações (Passo Inicial):**
   - Transcreva as models Python presentes em `app/models.py`. 
   - Adapte a Foreign Key de `user_id` para `company_id`.
   - Adicione os `properties` (properties decorators/calculados) como o `current_invoice` para que a API já devolva os somatórios feitos de forma nativa e protegida.

2. **Rotas de API REST:**
   - Crie um Controller/Blueprint específico para o Financeiro.
   - Tenha endpoints paginados (Pessoas jurídicas têm MUITO mais transações que pessoas físicas. Sem paginação, a tela de lançamentos irá travar o navegador rapidamente).
   - Use filtros via Query Strings SQL: ex: `/api/transactions?month=10&year=2026&company_id=123`.

3. **Front-end Estrutural:**
   - Crie o menu na sua Sidebar existente.
   - Defina um componente `LayoutFinanceiro` que recebe a rota filho (as subabas de Lançamentos, Dashboard, etc).
   - Use abas nativas HTML superiores ou sub-menus na sidebar para a navegação interna.

4. **Regras de Validação Cruciais para o seu Front-end Web:**
   - Nunca permitir lançar despesa sem estar associada a uma `Account` válida. (Seja banco ou cartão de crédito).
   - Fazer tratamento na tela de "Data": O usuário frequentemente insere lançamentos com datas retroativas (esqueceram de lançar na sexta passada). Certifique-se de que a ordenação das tabelas front-end priorize a `data da transação (date)` e não a `data de criação (created_at)` no banco.

---

*Focado em tornar o fluxo coeso e livre de redundâncias. Se precisar implementar código backend (Flask/Node/etc) ou frontend (Vue/React) para as telas citadas acima, me avise o framework escolhido para iniciarmos a programação.*
