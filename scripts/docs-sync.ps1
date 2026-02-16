# Docs Sync Script

\C:\InfinityMesh\docs = "C:\InfinityMesh\docs"

\ = Get-Content "\C:\InfinityMesh\docs\SYNC_MANIFEST.json" | ConvertFrom-Json
\.last_sync = Get-Date -Format s
\ | ConvertTo-Json -Depth 10 | Out-File "\C:\InfinityMesh\docs\SYNC_MANIFEST.json" -Force

Write-Host "Documentation Sync Complete." -ForegroundColor Green
