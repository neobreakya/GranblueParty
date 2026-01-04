#!/usr/bin/env node
// Generate config.js from environment variables during deployment

const fs = require('fs');
const path = require('path');

const configContent = `// Auto-generated config from environment variables
// This file is created during npm install (postinstall hook)

const config = {
  // To configure CORS headers
  frontend: {
    url: process.env.FRONTEND_URL || 'http://localhost',
    port: process.env.FRONTEND_PORT || 4000,
  },
  // Express port
  app: {
    port: process.env.PORT || 3000,
  },
  // PostgreSQL DB
  db: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    name: process.env.DB_NAME || 'gbf',
    user: process.env.DB_USER || 'pguser',
    password: process.env.DB_PASSWORD || 'gbfparser',
    // Absolute path where the version file of the DB is
    versionFile: process.env.DB_VERSION_FILE || 'db.version',
  },
  jwt: {
    // 512 bits key minimum.
    secret: process.env.JWT_SECRET || 'my secret secret',
    BCRYPT_SALT_ROUNDS: 12,
    secureCookie: process.env.NODE_ENV === 'production', // HTTPS only in production
  },
  // https://github.com/mailjet/mailjet-apiv3-nodejs
  mailinjet: {
    public_key: process.env.MAILJET_PUBLIC || '',
    private_key: process.env.MAILJET_PRIVATE || '',
  },
  logs: process.env.LOGS_DIR || 'API/logs',
};

module.exports = config;
`;

const configPath = path.join(__dirname, '../src/config.js');
fs.writeFileSync(configPath, configContent);
console.log('✓ Generated src/config.js from environment variables');
