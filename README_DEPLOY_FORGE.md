# Deploy remoto via Forge — FGInovaigestao

Este projeto pode ser atualizado remotamente pelo fluxo:

1. Forge/OpenClaw altera o código.
2. Forge faz `git add`, `git commit` e `git push` no repositório.
3. A máquina Windows onde o sistema roda executa periodicamente `deployment/forge-deploy.ps1`.
4. O script verifica se existe commit novo.
5. Se **não houver atualização**, ele encerra sem reiniciar nada.
6. Se **houver atualização**, ele faz `git pull --ff-only`, roda comandos opcionais e reinicia somente o serviço NSSM `GestaoInova`.

## Regra principal

O serviço **só é reiniciado se o Git realmente tiver commit novo**.

Se o repositório local já estiver atualizado, o script registra:

```text
Already up to date. Nenhum pull, nenhum build, nenhum restart.
```

Isso evita queda desnecessária do sistema.

---

## Arquivos criados

```text
deployment/forge-deploy.ps1       # Script PowerShell de deploy seguro
forge-deploy.env.example          # Exemplo de configuração local
README_DEPLOY_FORGE.md            # Esta documentação
```

O arquivo real `forge-deploy.env` deve ser criado na máquina Windows copiando o exemplo:

```powershell
Copy-Item .\forge-deploy.env.example .\forge-deploy.env
```

Depois ajuste se necessário.

---

## Configuração padrão para este projeto

```env
PROJECT_NAME=FGInovaigestao
GIT_REMOTE=origin
GIT_BRANCH=main
SERVICE_MANAGER=nssm
SERVICE_NAME=GestaoInova
PRE_DEPLOY_COMMAND=
BUILD_COMMAND=
MIGRATE_COMMAND=
HEALTHCHECK_URL=
HEALTHCHECK_ATTEMPTS=6
HEALTHCHECK_DELAY_SECONDS=5
```

### Importante

- O script não mexe no Nginx.
- O script não mexe em outros projetos.
- O script roda dentro da pasta deste projeto.
- Cada projeto continua com seu próprio `.env`, banco e arquivos.
- O Nginx pode continuar compartilhado entre vários sistemas sem ser reiniciado.

---

## Como testar manualmente no Windows

Abra PowerShell na raiz do projeto e rode:

```powershell
powershell -ExecutionPolicy Bypass -File .\deployment\forge-deploy.ps1
```

Se não houver commit novo, ele deve terminar sem restart.

---

## Como agendar no Windows

### Opção recomendada: Agendador de Tarefas

Criar uma tarefa recorrente a cada 2, 5 ou 10 minutos.

Programa:

```text
powershell.exe
```

Argumentos:

```text
-ExecutionPolicy Bypass -File "C:\CAMINHO\DO\PROJETO\deployment\forge-deploy.ps1"
```

Iniciar em:

```text
C:\CAMINHO\DO\PROJETO
```

Troque `C:\CAMINHO\DO\PROJETO` pelo caminho real da pasta do FGInovaigestao na máquina Windows.

---

## Pré-requisitos na máquina Windows

A máquina precisa ter:

- Git instalado e disponível no PATH;
- PowerShell;
- NSSM instalado e disponível no PATH;
- serviço NSSM chamado exatamente `GestaoInova`;
- acesso ao GitHub para fazer `git fetch`/`git pull`;
- repositório local na branch `main`;
- working tree limpa, sem alterações locais não commitadas.

---

## Segurança operacional

O script aborta sem reiniciar se:

- estiver em branch diferente da configurada;
- houver alterações locais não commitadas;
- o histórico remoto exigir merge não fast-forward;
- `git pull --ff-only` falhar;
- build/migration configurado falhar;
- `nssm restart GestaoInova` falhar;
- healthcheck configurado falhar.

---

## Fluxo ideal pelo Telegram/Forge

Pedido sugerido:

```text
@Openfogebot no projeto FGInovaigestao, faça o ajuste X.
Use o repo correto, teste o mínimo necessário, faça commit e push.
Não reinicie serviço diretamente pelo Telegram.
A rotina local de deploy vai puxar o commit e reiniciar o GestaoInova somente se houver atualização.
```

---

## Sobre build e migrations

Se no futuro este projeto precisar rodar comandos antes do restart, configure no `forge-deploy.env` local:

```env
BUILD_COMMAND=pip install -r requirements.txt
MIGRATE_COMMAND=python migrate.py
```

Ou deixe vazio para apenas `git pull` + `nssm restart GestaoInova` quando houver commit novo.

---

## Primeira aplicação

Para começar com segurança:

1. copiar `forge-deploy.env.example` para `forge-deploy.env` na máquina Windows;
2. rodar o script manualmente;
3. confirmar que, sem commit novo, ele não reinicia;
4. fazer um commit pequeno de teste;
5. rodar novamente e confirmar pull + restart;
6. só depois criar a tarefa recorrente no Agendador.
