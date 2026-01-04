import express from 'express';
import { exec } from 'child_process';
import fs from 'fs';
import path from 'path';

const router = express.Router();

router.use(express.json()); // For parsing application/json body

// Base route: /admin

router.get('/weapons', (req, res) => {
  req.context.models.getAdminWeapons(req, res);
});

router.post('/weapons', (req, res) => {
  req.context.models.saveAdminWeapons(req, res);
});

router.get('/summons', (req, res) => {
  req.context.models.getAdminSummons(req, res);
});

router.post('/summons', (req, res) => {
  req.context.models.saveAdminSummons(req, res);
});

/**
 * POST /admin/sync-database
 * Restores database from backup file
 * Body: { backupFilePath: string, adminSecret: string }
 */
router.post('/sync-database', (req, res) => {
  const { backupFilePath, adminSecret } = req.body;
  const ADMIN_SECRET = process.env.ADMIN_SECRET || 'change-me-in-production';

  // Security check
  if (adminSecret !== ADMIN_SECRET) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (!backupFilePath) {
    return res.status(400).json({ error: 'backupFilePath is required' });
  }

  // For GitHub Actions: read from workspace root
  // For local: use provided absolute path
  let filePath = backupFilePath;
  if (!path.isAbsolute(filePath)) {
    filePath = path.join(process.cwd(), '..', '..', filePath);
  }

  // Validate file exists
  if (!fs.existsSync(filePath)) {
    return res.status(400).json({ error: `File not found: ${filePath}` });
  }

  // Build psql restore command using DATABASE_URL
  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) {
    return res
      .status(500)
      .json({ error: 'DATABASE_URL environment variable not set' });
  }

  const psqlCmd = `psql "${databaseUrl}" -f "${filePath}"`;

  exec(psqlCmd, { timeout: 300000 }, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({
        error: 'Database restore failed',
        message: stderr || error.message,
      });
    }

    res.json({
      success: true,
      message: 'Database restored successfully',
      output: stdout,
    });
  });
});

export default router;
