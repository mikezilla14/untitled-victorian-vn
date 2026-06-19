# Register a Windows Scheduled Task to run the daily asset manifest update at 6:15 AM local time.
#
# Usage (run from an elevated or normal PowerShell — current user context):
#   .\scripts\register_daily_asset_manifest_task.ps1
#   .\scripts\register_daily_asset_manifest_task.ps1 -Time "06:15" -Unregister
#
# Requires: Python on PATH (py launcher or python).

param(
    [string]$Time = "06:15",
    [string]$TaskName = "VictorianVN-DailyAssetManifest",
    [switch]$Unregister
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$RunnerScript = Join-Path $RepoRoot "scripts\run_daily_asset_manifest.ps1"

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
    -Description "Daily asset manifest and reconciliation report for untitled-victorian-vn." `
    -Force | Out-Null

Write-Host ("Registered scheduled task '{0}' daily at {1} (local time)." -f $TaskName, $Time)
Write-Host "Runner: $RunnerScript"
Write-Host "Report: assets_source/approved_assets/daily_asset_manifest.md"
Write-Host ""
Write-Host "Test now: .\scripts\run_daily_asset_manifest.ps1"
Write-Host 'Remove:   .\scripts\register_daily_asset_manifest_task.ps1 -Unregister'
