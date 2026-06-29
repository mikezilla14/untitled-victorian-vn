# Run the daily standup ceremony and write a dated markdown report.
# Used by Windows Task Scheduler (see register_daily_standup_task.ps1).

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$LogDir = Join-Path $RepoRoot "main-game\draft\releases\planning\standups"
$LogFile = Join-Path $LogDir "scheduler.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-Log {
    param([string]$Message)
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$stamp $Message" | Add-Content -Path $LogFile -Encoding utf8
}

try {
    Set-Location $RepoRoot
    Write-Log "Starting daily standup"

    $py = Get-Command py -ErrorAction SilentlyContinue
    if (-not $py) {
        $py = Get-Command python -ErrorAction SilentlyContinue
    }
    if (-not $py) {
        throw "Python not found on PATH (tried py and python)"
    }

    & $py.Source (Join-Path $RepoRoot "scripts\daily_standup.py") --report --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "daily_standup.py exited with code $LASTEXITCODE"
    }

    Write-Log "Standup report written successfully"
    exit 0
}
catch {
    Write-Log "ERROR: $_"
    exit 1
}
