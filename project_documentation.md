# Documentação do Projeto: Sistema Inadimplência OAZ

Este documento contém as informações necessárias para preenchimento do formulário de gestão de projetos, baseado na análise técnica completa do sistema desenvolvido.

---

## 1. Contexto e Justificativa

### Descrição Resumida
Sistema web integrado para gestão automatizada de contas a receber, focado na redução de inadimplência. A solução automatiza o ciclo completo: ingestão de notas fiscais (NFe), enriquecimento com boletos bancários (PDF), disponibilização em portal de autoatendimento para clientes e baixa automática via conciliação bancária (CNAB/OFX).

### Problema/Oportunidade
**Problema:** Alta carga operacional manual para correlacionar notas fiscais com seus respectivos boletos e, posteriormente, confirmar os pagamentos recebidos pelo banco. Dificuldade dos clientes finais em acessarem 2ª via de boletos, gerando atrito e atrasos.
**Oportunidade:** Automatizar o fluxo de dados fiscal e bancário para reduzir erros de conciliação, agilizar a disponibilização de cobranças e dar transparência financeira em tempo real.

### Objetivos
1.  **Eliminar Digitação Manual:** Automatizar 100% da criação de clientes e contas a receber via importação de XML NFe.
2.  **Centralização de Cobrança:** Vincular automaticamente PDFs de boletos às faturas corretas usando OCR e leitura de código de barras.
3.  **Autoatendimento:** Oferecer um portal onde o inadimplente possa baixar seus boletos sem intervenção humana.
4.  **Conciliação Ágil:** Processar arquivos de retorno bancário (.RET) para baixa automática de pagamentos com lógica de "fuzzy match".

### Alinhamento Estratégico
O projeto alinha-se à estratégia de **Eficiência Operacional** e **Transformação Digital** da empresa, reduzindo o Custo de Servir (Cost to Serve) da equipe financeira e melhorando a Experiência do Cliente (CX) através do portal self-service.

---

## 2. Escopo

### Escopo do Projeto (O que será feito)
O sistema é composto por 4 módulos principais:

1.  **Módulo de Ingestão Fiscal (NFe):**
    *   Parser de XML (NFe) para extração de dados cadastrais (Cliente, Endereço, Contato).
    *   Extração inteligente de Duplicatas para geração automática de "Contas a Receber" e parcelamento.
    *   Extração detalhada de Itens/Produtos para conferência.

2.  **Módulo de Enriquecimento (Boletos):**
    *   Upload em lote de PDFs de boletos bancários.
    *   Motor de OCR/Regex para leitura de linhas digitáveis e códigos de barra.
    *   Algoritmo de vinculação automática (Match) entre Boleto e Fatura (baseado em Valor + Data).

3.  **Módulo Portal do Cliente:**
    *   Área logada segura para clientes (login via CNPJ/CPF).
    *   Dashboard de faturas em aberto e histórico de pagamentos.
    *   Download direto de XMLs e PDFs de boletos.

4.  **Módulo de Conciliação Bancária:**
    *   Parser universal de arquivos de retorno (CNAB 240, CNAB 400, OFX, CSV).
    *   Motor de Conciliação com regras de "Match Exato" (Nosso Número) e "Fallback" (Valor + Data).
    *   Relatórios de divergência (valores pagos a menor/maior) e baixas automáticas.

### Fora do Escopo (O que NÃO será feito)
*   Emissão de Notas Fiscais (o sistema apenas importa notas já emitidas).
*   Geração de remessa bancária (geração de boletos novos); o sistema trabalha com boletos já gerados por outro ERP/Banco.
*   Integração direta via API com bancos (a troca de dados é via arquivos).
*   Gestão de estoques ou contabilidade fiscal avançada (SPED, etc).

### Premissas
*   O usuário possui acesso aos arquivos XML das notas fiscais emitidas.
*   O usuário possui acesso aos arquivos PDF dos boletos e arquivos .RET do banco.
*   Infraestrutura baseada em container ou VM Linux/Windows com suporte a Python 3.9+.

### Restrições
*   **Formatos Bancários:** O parser detalhado é otimizado para padrões Itaú e Bradesco (CNAB 400/240), com suporte genérico para outros bancos.
*   **Volume de Dados:** O processamento de grandes lotes (milhares de arquivos simultâneos) depende da capacidade de I/O do servidor, rodando em background.
*   **Identificadores:** A conciliação automática exata depende da presença do "Nosso Número" correto no boleto ou da integridade dos valores.
