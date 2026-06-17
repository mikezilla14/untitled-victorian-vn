# Daily standup reports

Dated standup artifacts from `scripts/daily_standup.py --report`:

- `daily_standup_YYYY-MM-DD.md` — one file per report date
- `scheduler.log` — Windows Task Scheduler run log (if registered)
- `../daily_standup_report.md` — always points at the most recent run

## Run manually

```powershell
py scripts/daily_standup.py --report
```

## Schedule daily at 6:00 AM (Windows)

```powershell
./scripts/register_daily_standup_task.ps1
./scripts/run_daily_standup.ps1   # optional smoke test
```

Unregister:

```powershell
./scripts/register_daily_standup_task.ps1 -Unregister
```
