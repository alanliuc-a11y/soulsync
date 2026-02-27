# SoulSync

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SoulSync is a **cross-bot soul synchronization system**. It allows your AI assistants (like OpenClaw) to share the same memory, personality, and skills across multiple devices and platforms.

## Features

- **Cloud-based memory storage** – All memories are stored in the cloud, accessible from anywhere.
- **Real-time synchronization** – Changes are instantly synced via WebSocket.
- **Multi-bot support** – Currently supports OpenClaw; more bots (CoPaw, etc.) coming soon.
- **Subscription model** – 7-day free trial, then $1/month.
- **Lightweight & easy to deploy** – Node.js backend + SQLite database.

## Project Structure

```
soulsync/
├── server/              # Node.js backend
│   ├── src/
│   ├── package.json
│   └── soulsync.db      # SQLite database (ignored by git)
├── plugins/
│   ├── base/            # Base classes for future bots
│   └── openclaw/        # OpenClaw plugin
│       ├── src/
│       ├── config.json.example
│       └── requirements.txt
└── README.md
```

## Getting Started

### 1. Deploy the backend

On your cloud server (e.g., Aliyun ECS), run:

```bash
cd server
npm install
node src/index.js
```

For production, use PM2:

```bash
npm install -g pm2
pm2 start src/index.js --name soulsync
pm2 save
pm2 startup
```

Make sure port 3000 is open in your firewall / security group.

### 2. Install the OpenClaw plugin

```bash
openclaw plugins install soulsync
```

Or install from local directory:

```bash
openclaw plugins install /path/to/soulsync/plugins/openclaw
```

### 3. Configure the plugin

Edit `~/.openclaw/extensions/soulsync/config.json`:

```json
{
  "cloud_url": "http://your-server:3000",
  "email": "your-email@example.com",
  "password": "your-password"
}
```

### 4. Start the plugin

```bash
openclaw soulsync:start
```

## How It Works

SoulSync creates a persistent memory layer for your AI assistants:

1. **Memory Files** – Store your bot's identity, skills, and memories in Markdown files
2. **Cloud Sync** – All changes are automatically uploaded to the cloud
3. **Multi-Device** – Access the same memory from any device with OpenClaw installed
4. **Real-time** – WebSocket connection ensures instant synchronization

## Documentation

- [Installation Guide](plugins/openclaw/INSTALL.md)
- [Troubleshooting](plugins/openclaw/TROUBLESHOOTING.md)
- [Deployment Checklist](plugins/openclaw/DEPLOY_CHECKLIST.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.
