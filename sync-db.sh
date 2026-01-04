#!/bin/bash
# Database sync helper script
# Usage: ./sync-db.sh [backup-file-path]

set -e

BACKUP_FILE="${1:-gbf_backup.sql}"
GITHUB_REPO="neobreakya/GranblueParty"  # Update with your repo
BRANCH="main"

echo "📦 Database Sync Helper"
echo "======================"

# Step 1: Verify backup exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: Backup file not found: $BACKUP_FILE"
    echo "Usage: ./sync-db.sh [path-to-backup]"
    exit 1
fi

FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "✓ Found backup: $BACKUP_FILE ($FILE_SIZE)"

# Step 2: Check git status
echo ""
echo "📝 Git Status:"
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠ Uncommitted changes detected"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 3: Add and commit backup
echo ""
echo "📤 Uploading backup to GitHub..."
git add "$BACKUP_FILE"
git commit -m "Database backup: $(date +'%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin $BRANCH

echo "✓ Pushed to GitHub"

# Step 4: Trigger GitHub Action
echo ""
echo "🚀 Triggering GitHub Actions workflow..."
echo ""
echo "Visit: https://github.com/$GITHUB_REPO/actions"
echo "to monitor the sync progress"
echo ""
echo "The workflow will:"
echo "  1. Download the backup from GitHub"
echo "  2. Call your Railway API to sync the database"
echo "  3. Update your production database"
echo ""
echo "✓ All done! Check GitHub Actions for progress."
