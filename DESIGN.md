# FGinovaigestao — Design System

## 1. Visual Theme & Atmosphere

FGinovaigestao deve parecer uma **central operacional premium em dark mode**.

A direção visual mistura três referências:
- **Linear** para estrutura, hierarquia e legibilidade de produto B2B
- **Spotify** para atmosfera escura, presença visual e uso funcional do verde
- **Raycast** para profundidade, superfícies premium e microinterações

A regra central é simples:

> o sistema base é sóbrio, escuro e contido; a cor forte fica reservada para ação importante e alertas operacionais.

Não é uma interface “decorativa”. É uma cabine de comando. Os elementos precisam passar:
- clareza
- velocidade de leitura
- sensação de software forte
- contraste limpo
- prioridade visual inequívoca

## 2. Core Principles

### 2.1 Product-first, not marketing-first
A interface deve parecer um produto de uso diário, não uma landing page.

### 2.2 Dark surfaces in layers
O escuro não é um bloco único. Deve haver camadas:
- fundo profundo
- painel
- card
- card elevado
- modal

### 2.3 Accent color is functional
O verde principal é para:
- item ativo
- CTA principal
- estado positivo
- foco importante

Não usar verde como decoração genérica.

### 2.4 Operational alerts outrank aesthetics
Alertas do sistema têm prioridade total sobre o design.

Se um card/status/notificação usa cor operacional, o resto da UI deve recuar.

### 2.5 Premium depth, not noisy glow
Profundidade com sombra, borda sutil e contraste de superfície.
Glow exagerado só em estados pontuais.

## 3. Color Palette

### App foundation
- **App Void**: `#0b0d0f` — fundo global
- **Sidebar Deep**: `#0f1317` — sidebar e áreas estruturais
- **Panel Surface**: `#121820` — painéis principais
- **Card Surface**: `#171d25` — cards e blocos
- **Card Hover**: `#1d2530` — hover e áreas elevadas
- **Elevated Surface**: `#202a35` — dropdowns, elementos em destaque

### Text
- **Text Strong**: `#f5f7fa`
- **Text Base**: `#d9e0e8`
- **Text Muted**: `#9aa6b2`
- **Text Faint**: `#6f7c89`

### Borders
- **Border Subtle**: `rgba(255,255,255,0.06)`
- **Border Strong**: `rgba(255,255,255,0.12)`
- **Inset Highlight**: `rgba(255,255,255,0.05)`

### Brand / Action
- **Primary Green**: `#1ed760`
- **Primary Green Hover**: `#1fef6d`
- **Primary Green Soft**: `rgba(30,215,96,0.16)`

### Focus / Info
- **Info Blue**: `#60a5fa`
- **Info Blue Soft**: `rgba(96,165,250,0.18)`

### Operational semantics
Essas cores são reservadas para estados semânticos reais:
- **Danger**: `#f87171`
- **Warning**: `#f59e0b`
- **Success**: `#22c55e`
- **Info**: `#38bdf8`

### Alert preservation rule
Nunca neutralizar, pastelizar ou “embelezar” alertas críticos a ponto de perder leitura.

## 4. Typography

### Font family
Usar stack limpa e moderna:
`Inter, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif`

### Hierarchy
- **Page Title**: 28–32px / 700
- **Section Title**: 20–24px / 700
- **Card Title**: 16–18px / 600
- **Body**: 14–16px / 400–500
- **Meta / Labels**: 12–13px / 500
- **Micro**: 11–12px / 500

### Type rules
- títulos: peso forte, sem exagero
- textos de apoio: mais frios e discretos
- labels e navegação: ligeiro tracking positivo quando fizer sentido
- evitar blocos muito claros e muito densos ao mesmo tempo

## 5. Surfaces & Elevation

### Radius scale
- **Small**: 10px
- **Medium**: 14px
- **Large**: 18px
- **Pill**: 999px

### Shadow system
- **Soft panel**: `0 10px 30px rgba(0,0,0,0.22)`
- **Card**: `0 14px 40px rgba(0,0,0,0.24)`
- **Modal**: `0 24px 80px rgba(0,0,0,0.42)`
- **Inset premium line**: `inset 0 1px 0 rgba(255,255,255,0.04)`

## 6. Component Rules

### Sidebar
- mais escura que o conteúdo
- borda lateral sutil
- item ativo com:
  - fundo verde suave
  - texto claro
  - leve glow ou halo discreto
  - sensação de item “energizado”

### Topbar
- translúcida ou semitranslúcida em dark
- borda inferior sutil
- precisa parecer premium e leve

### Cards
- fundo escuro em camada acima do painel
- borda quase invisível
- sombra leve
- hover com leve elevação e clareamento

### Buttons
#### Primary
- verde funcional
- texto escuro
- pill ou radius médio
- hover mais vivo

#### Secondary
- fundo escuro elevado
- texto claro
- borda sutil

#### Ghost
- quase invisível, só com hover

### Inputs
- fundo escuro
- borda sutil
- foco com azul suave ou verde, sem neon exagerado
- erro com borda vermelha clara e contraste forte

### Modals
- mais elevados que cards
- fundo escuro limpo
- foco visual no conteúdo
- excelente contraste para formulários

### Badges / Chips
- usar versões discretas por padrão
- cores fortes só quando carregarem significado real

## 7. Notifications & Alerts

### Critical rule
As notificações piscantes/coloridas atuais são parte do sistema operacional do produto.

Portanto:
- manter comportamento
- manter distinção cromática
- não rebaixar a prioridade visual
- integrar ao novo visual apenas com moldura/sombra/borda melhores

### Alert styling direction
O shell do alerta pode ficar mais sofisticado, mas o núcleo semântico da cor precisa continuar óbvio.

## 8. Pages

### Dashboard
- cara de centro de comando
- cards fortes, limpos, legíveis
- números principais com destaque
- contexto secundário mais discreto

### Projetos
- cards com leitura rápida
- status, nome, cliente e sinais operacionais bem escaneáveis

### Kanban
- visual mais premium
- sem quebrar densidade e produtividade
- foco em contraste e arraste intuitivo

### Admin / Usuários
- modais e formulários mais confiáveis
- validações mais claras
- visual mais forte em permissões e estados

## 9. Do
- usar o verde com inteligência, não em excesso
- manter o fundo escuro em múltiplas camadas
- priorizar clareza operacional
- aplicar profundidade elegante
- deixar alertas semânticos dominarem quando necessário

## 10. Don’t
- não transformar o sistema em clone de player de música
- não usar gradiente/colorido em tudo
- não sacrificar leitura por estilo
- não competir visualmente com alertas críticos
- não fazer cards claros demais ou lavados demais
