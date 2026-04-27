<#
.SYNOPSIS
  Deploy seguro do FGInovaigestao para servidor Windows/NSSM.

.DESCRIPTION
  - Faz git fetch.
  - Compara HEAD local com origin/BRANCH.
  - Se estiver already up to date, NÃO reinicia o serviço.
  - Se houver commit novo, faz git pull --ff-only.
  - Opcionalmente roda build/migration.
  - Reinicia somente o serviço NSSM configurado, sem mexer no Nginx.
  - Escreve logs locais em deployment/logs.

USO MANUAL:
  powershell -ExecutionPolicy Bypass -File .\deployment\forge-deploy.ps1

USO AGENDADO:
  Criar uma tarefa no Agendador de Tarefas chamando o comando acima na raiz do projeto.
#>

param(
  [string]$ConfigPath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$DefaultConfigPath = Join-Path $RepoRoot "forge-deploy.env"
if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
  $ConfigPath = $DefaultConfigPath
}

$LogDir = Join-Path $ScriptDir "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("forge-deploy-{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))
$LockFile = Join-Path $ScriptDir "forge-deploy.lock"

function Write-Log {
  param([string]$Message, [string]$Level = "INFO")
  $line = "{0} [{1}] {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Level, $Message
  Write-Host $line
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

function Load-EnvFile {
  param([string]$Path)
  $cfg = @{}
  if (-not (Test-Path $Path)) {
    Write-Log "Config não encontrada em $Path; usando defaults seguros."
    return $cfg
  }

  Get-Content $Path | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#")) { return }
    $idx = $line.IndexOf("=")
    if ($idx -lt 1) { return }
    $key = $line.Substring(0, $idx).Trim()
    $value = $line.Substring($idx + 1).Trim()
    if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
      $value = $value.Substring(1, $value.Length - 2)
    }
    $cfg[$key] = $value
  }
  return $cfg
}

function Get-Cfg {
  param($Cfg, [string]$Key, [string]$Default = "")
  if ($Cfg.ContainsKey($Key) -and -not [string]::IsNullOrWhiteSpace([string]$Cfg[$Key])) {
    return [string]$Cfg[$Key]
  }
  return $Default
}

function Run-Git {
  param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)

  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = "git"
  foreach ($arg in $Args) { [void]$psi.ArgumentList.Add($arg) }
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.UseShellExecute = $false
  $psi.CreateNoWindow = $true

  $proc = New-Object System.Diagnostics.Process
  $proc.StartInfo = $psi
  [void]$proc.Start()
  $stdout = $proc.StandardOutput.ReadToEnd()
  $stderr = $proc.StandardError.ReadToEnd()
  $proc.WaitForExit()
  $code = $proc.ExitCode

  if ($stdout) { $stdout.TrimEnd().Split("`n") | ForEach-Object { if ($_.Trim()) { Write-Log "git $($Args -join ' ') stdout: $($_.TrimEnd())" } } }
  if ($stderr) { $stderr.TrimEnd().Split("`n") | ForEach-Object { if ($_.Trim()) { Write-Log "git $($Args -join ' ') stderr: $($_.TrimEnd())" } } }
  if ($code -ne 0) { throw "git $($Args -join ' ') falhou com código $code" }
  return $stdout
}

function Invoke-OptionalCommand {
  param([string]$Name, [string]$Command)
  if ([string]::IsNullOrWhiteSpace($Command)) { return }
  Write-Log "Executando ${Name}: $Command"
  cmd.exe /c $Command 2>&1 | ForEach-Object { Write-Log "${Name}: $_" }
  if ($LASTEXITCODE -ne 0) { throw "$Name falhou com código $LASTEXITCODE" }
}

function Test-Healthcheck {
  param([string]$Url, [int]$Attempts, [int]$DelaySeconds)
  if ([string]::IsNullOrWhiteSpace($Url)) {
    Write-Log "Healthcheck não configurado; deploy finalizado sem checagem HTTP."
    return
  }

  for ($i = 1; $i -le $Attempts; $i++) {
    try {
      Write-Log "Healthcheck tentativa $i/${Attempts}: $Url"
      $res = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 10
      if ($res.StatusCode -ge 200 -and $res.StatusCode -lt 500) {
        Write-Log "Healthcheck OK: HTTP $($res.StatusCode)"
        return
      }
      Write-Log "Healthcheck retornou HTTP $($res.StatusCode)" "WARN"
    } catch {
      Write-Log "Healthcheck falhou: $($_.Exception.Message)" "WARN"
    }
    Start-Sleep -Seconds $DelaySeconds
  }
  throw "Healthcheck falhou após $Attempts tentativa(s)."
}

function Wait-ServiceState {
  param(
    [string]$Name,
    [string]$DesiredStatus,
    [int]$TimeoutSeconds = 90
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  do {
    $svc = Get-Service -Name $Name -ErrorAction Stop
    Write-Log "Serviço ${Name} status atual: $($svc.Status); aguardando $DesiredStatus"
    if ($svc.Status.ToString() -eq $DesiredStatus) {
      return
    }
    Start-Sleep -Seconds 3
  } while ((Get-Date) -lt $deadline)

  $final = (Get-Service -Name $Name -ErrorAction Stop).Status
  throw "Timeout aguardando serviço ${Name} ficar ${DesiredStatus}. Status final: $final"
}

function Restart-NssmServiceSafely {
  param([string]$Name)

  $svc = Get-Service -Name $Name -ErrorAction Stop
  Write-Log "Status inicial do serviço ${Name}: $($svc.Status)"

  if ($svc.Status -eq 'StopPending') {
    Write-Log "Serviço já está parando; aguardando parar."
    Wait-ServiceState -Name $Name -DesiredStatus "Stopped" -TimeoutSeconds 120
  } elseif ($svc.Status -eq 'StartPending') {
    Write-Log "Serviço já está iniciando; aguardando ficar Running antes de reiniciar."
    Wait-ServiceState -Name $Name -DesiredStatus "Running" -TimeoutSeconds 120
  }

  $svc = Get-Service -Name $Name -ErrorAction Stop
  if ($svc.Status -eq 'Running') {
    Write-Log "Parando serviço NSSM: ${Name}"
    & nssm stop $Name 2>&1 | ForEach-Object { Write-Log "nssm stop: $_" }
    $stopCode = $LASTEXITCODE
    if ($stopCode -ne 0) {
      Write-Log "nssm stop retornou código $stopCode; vou checar o status antes de abortar." "WARN"
    }
    Wait-ServiceState -Name $Name -DesiredStatus "Stopped" -TimeoutSeconds 120
  } elseif ($svc.Status -ne 'Stopped') {
    throw "Serviço ${Name} está em status inesperado antes do start: $($svc.Status)"
  }

  Write-Log "Iniciando serviço NSSM: ${Name}"
  & nssm start $Name 2>&1 | ForEach-Object { Write-Log "nssm start: $_" }
  $startCode = $LASTEXITCODE
  if ($startCode -ne 0) {
    Write-Log "nssm start retornou código $startCode; vou checar o status antes de abortar." "WARN"
  }
  Wait-ServiceState -Name $Name -DesiredStatus "Running" -TimeoutSeconds 120
}

# Lock simples para evitar deploy simultâneo.
$lockStream = $null
try {
  $lockStream = [System.IO.File]::Open($LockFile, 'OpenOrCreate', 'ReadWrite', 'None')
} catch {
  Write-Log "Outro deploy já está em execução. Saindo sem fazer nada." "WARN"
  exit 0
}

try {
  Set-Location $RepoRoot
  Write-Log "==== Iniciando forge-deploy FGInovaigestao ===="
  Write-Log "RepoRoot: $RepoRoot"

  $cfg = Load-EnvFile $ConfigPath
  $Remote = Get-Cfg $cfg "GIT_REMOTE" "origin"
  $Branch = Get-Cfg $cfg "GIT_BRANCH" "main"
  $ServiceManager = (Get-Cfg $cfg "SERVICE_MANAGER" "nssm").ToLowerInvariant()
  $ServiceName = Get-Cfg $cfg "SERVICE_NAME" "GestaoInova"
  $PreDeployCommand = Get-Cfg $cfg "PRE_DEPLOY_COMMAND" ""
  $BuildCommand = Get-Cfg $cfg "BUILD_COMMAND" ""
  $MigrateCommand = Get-Cfg $cfg "MIGRATE_COMMAND" ""
  $HealthcheckUrl = Get-Cfg $cfg "HEALTHCHECK_URL" ""
  $HealthcheckAttempts = [int](Get-Cfg $cfg "HEALTHCHECK_ATTEMPTS" "6")
  $HealthcheckDelaySeconds = [int](Get-Cfg $cfg "HEALTHCHECK_DELAY_SECONDS" "5")

  Write-Log "Config: remote=$Remote branch=$Branch serviceManager=$ServiceManager serviceName=$ServiceName"

  $currentBranch = (& git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($currentBranch)) {
    throw "Não consegui identificar a branch atual."
  }
  if ($currentBranch -ne $Branch) {
    throw "Branch atual é '$currentBranch', mas deploy espera '$Branch'. Não vou fazer pull/restart."
  }

  # Só alterações em arquivos rastreados devem bloquear deploy.
  # Arquivos untracked de runtime/upload/cache devem ser ignorados pelo .gitignore.
  $trackedDirty = (& git status --porcelain --untracked-files=no)
  if ($trackedDirty) {
    Write-Log "Working tree possui alterações locais em arquivos rastreados. Abortando para não sobrescrever nada:" "ERROR"
    $trackedDirty | ForEach-Object { Write-Log $_ "ERROR" }
    exit 2
  }

  $untracked = (& git ls-files --others --exclude-standard)
  if ($untracked) {
    Write-Log "Arquivos locais não rastreados ignorados pelo deploy:"
    $untracked | ForEach-Object { Write-Log "untracked: $_" }
  }

  Run-Git fetch $Remote $Branch | Out-Null

  $local = (& git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw "Falha ao ler HEAD local." }
  $remoteRef = "$Remote/$Branch"
  $remoteHead = (& git rev-parse $remoteRef).Trim()
  if ($LASTEXITCODE -ne 0) { throw "Falha ao ler $remoteRef." }

  Write-Log "HEAD local:  $local"
  Write-Log "HEAD remoto: $remoteHead"

  if ($local -eq $remoteHead) {
    Write-Log "Already up to date. Nenhum pull, nenhum build, nenhum restart."
    exit 0
  }

  & git merge-base --is-ancestor HEAD $remoteRef
  if ($LASTEXITCODE -ne 0) {
    throw "Histórico remoto não é fast-forward a partir do local. Abortando para evitar merge automático."
  }

  Invoke-OptionalCommand "pre-deploy" $PreDeployCommand
  Run-Git pull --ff-only $Remote $Branch | Out-Null

  Invoke-OptionalCommand "build" $BuildCommand
  Invoke-OptionalCommand "migration" $MigrateCommand

  switch ($ServiceManager) {
    "nssm" {
      Write-Log "Reiniciando serviço NSSM com espera segura: $ServiceName"
      Restart-NssmServiceSafely -Name $ServiceName
    }
    "none" {
      Write-Log "SERVICE_MANAGER=none; atualização aplicada sem restart." "WARN"
    }
    default {
      throw "SERVICE_MANAGER '$ServiceManager' não suportado neste script Windows. Use nssm ou none."
    }
  }

  Test-Healthcheck $HealthcheckUrl $HealthcheckAttempts $HealthcheckDelaySeconds
  Write-Log "Deploy concluído com sucesso."
  exit 0
} catch {
  Write-Log "Deploy falhou: $($_.Exception.Message)" "ERROR"
  exit 1
} finally {
  if ($null -ne $lockStream) { $lockStream.Close() }
}
