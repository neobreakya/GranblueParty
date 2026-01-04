# Database sync helper script (PowerShell version)
# Usage: .\sync-db.ps1 -BackupFile "gbf_backup.sql"

param(
    [string]$BackupFile = "gbf_backup.sql",
    [string]$GitBranch = "main"
)

$GitRepo = "neobreakya/GranblueParty"  # Update with your repo
$GitHubApiToken = $env:GITHUB_TOKEN

Write-Host "📦 Database Sync Helper"
Write-Host "======================" -ForegroundColor Cyan

# Step 1: Verify backup exists
if (-not (Test-Path $BackupFile)) {
    Write-Host "❌ Error: Backup file not found: $BackupFile" -ForegroundColor Red
    Write-Host "Usage: .\sync-db.ps1 -BackupFile 'path\to\backup.sql'"
    exit 1
}

$FileSize = (Get-Item $BackupFile).Length / 1MB
Write-Host "✓ Found backup: $BackupFile ($([Math]::Round($FileSize, 2)) MB)" -ForegroundColor Green

# Step 2: Check git status
Write-Host ""
Write-Host "📝 Git Status:"
$GitStatus = git status --porcelain
if ($GitStatus) {
    Write-Host "⚠ Uncommitted changes detected" -ForegroundColor Yellow
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne "y") {
        exit 1
    }
}

# Step 3: Add and commit backup
Write-Host ""
Write-Host "📤 Uploading backup to GitHub..."
git add $BackupFile
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Database backup: $timestamp" | Out-Null 2>&1
git push origin $GitBranch

Write-Host "✓ Pushed to GitHub" -ForegroundColor Green

# Step 4: Trigger GitHub Action (via workflow_dispatch)
Write-Host ""
Write-Host "🚀 Triggering GitHub Actions workflow..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Visit: https://github.com/$GitRepo/actions"
Write-Host "to monitor the sync progress"
Write-Host ""
Write-Host "The workflow will:"
Write-Host "  1. Download the backup from GitHub"
Write-Host "  2. Call your Railway API to sync the database"
Write-Host "  3. Update your production database"
Write-Host ""
Write-Host "✓ All done! Check GitHub Actions for progress." -ForegroundColor Green
