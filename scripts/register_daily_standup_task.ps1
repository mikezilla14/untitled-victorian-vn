# Register a Windows Scheduled Task to run the daily standup at 6:00 AM local time.
#
# Usage (run from an elevated or normal PowerShell — current user context):
#   .\scripts\register_daily_standup_task.ps1
#   .\scripts\register_daily_standup_task.ps1 -Time "06:00" -Unregister
#
# Requires: Python on PATH (py launcher or python).

param(
    [string]$Time = "06:00",
    [string]$TaskName = "VictorianVN-DailyStandup",
    [switch]$Unregister
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RunnerScript = Join-Path $RepoRoot "scripts\run_daily_standup.ps1"

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed scheduled task: $TaskName"
    exit 0
}

if (-not (Test-Path $RunnerScript)) {
    throw "Runner script not found: $RunnerScript"
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$RunnerScript`"" `
    -WorkingDirectory $RepoRoot

$trigger = New-ScheduledTaskTrigger -Daily -At $Time

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Daily MVP standup report for untitled-victorian-vn (dated markdown in planning/standups/)." `
    -Force | Out-Null

Write-Host ("Registered scheduled task '{0}' daily at {1} (local time)." -f $TaskName, $Time)
Write-Host "Runner: $RunnerScript"
Write-Host "Reports: main-game/draft/releases/planning/standups/daily_standup_YYYY-MM-DD.md"
Write-Host ""
Write-Host "Test now: .\scripts\run_daily_standup.ps1"
Write-Host 'Remove:   .\scripts\register_daily_standup_task.ps1 -Unregister'
