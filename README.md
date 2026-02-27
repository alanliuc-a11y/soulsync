# SoulSync

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🌐 [English](README_EN.md) | [中文](README_CN.md)

---

SoulSync is a **cross-bot soul synchronization system**. It allows your AI assistants (like OpenClaw) to share the same memory, personality, and skills across multiple devices and platforms.  

SoulSync 是一个**跨机器人灵魂同步系统**，让你的 AI 助理（如 OpenClaw）在多设备、多平台之间共享相同的记忆、人格和技能。



## Features / 功能特性



- **Cloud-based memory storage** – All memories are stored in the cloud, accessible from anywhere.  
  **云端记忆存储** – 所有记忆都存储在云端，随时随地可访问。

- **Real-time synchronization** – Changes are instantly synced via WebSocket.  
  **实时同步** – 通过 WebSocket 实现即时同步。

- **Multi-bot support** – Currently supports OpenClaw; more bots (CoPaw, etc.) coming soon.  
  **多机器人支持** – 目前已支持 OpenClaw，后续将支持 CoPaw 等更多机器人。

- **Subscription model** – 7-day free trial, then $1/month.  
  **订阅模式** – 7 天免费试用，之后每月 1 美元。

- **Lightweight & easy to deploy** – Node.js backend + SQLite database.  
  **轻量易部署** – Node.js 后端 + SQLite 数据库。



## Project Structure / 项目结构

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



## Getting Started / 快速开始



### 1. Deploy the backend / 部署后端



On your cloud server (e.g., Aliyun ECS), run:

在你的云服务器（如阿里云 ECS）上运行：

```bash
cd server
npm install
node src/index.js
```

For production, use PM2:

生产环境建议使用 PM2：

```bash
npm install -g pm2
pm2 start src/index.js --name soulsync
pm2 save
pm2 startup
```

Make sure port 3000 is open in your firewall / security group.

确保防火墙/安全组中已开放 3000 端口。



### 2. Install the OpenClaw plugin / 安装 OpenClaw 插件

```bash
openclaw plugins install soulsync
```

Or install from local directory:

或从本地目录安装：

```bash
openclaw plugins install /path/to/soulsync/plugins/openclaw
```



### 3. Configure the plugin / 配置插件

Edit `~/.openclaw/extensions/soulsync/config.json`:

编辑 `~/.openclaw/extensions/soulsync/config.json`：

```json
{
  "cloud_url": "http://your-server:3000",
  "email": "your-email@example.com",
  "password": "your-password"
}
```



### 4. Start the plugin / 启动插件

```bash
openclaw soulsync:start
```



## How It Works / 工作原理

SoulSync creates a persistent memory layer for your AI assistants:

SoulSync 为你的 AI 助理创建了一个持久化的记忆层：

1. **Memory Files** – Store your bot's identity, skills, and memories in Markdown files
   **记忆文件** – 将机器人的身份、技能和记忆存储在 Markdown 文件中
2. **Cloud Sync** – All changes are automatically uploaded to the cloud
   **云端同步** – 所有更改自动上传到云端
3. **Multi-Device** – Access the same memory from any device with OpenClaw installed
   **多设备** – 在任何安装了 OpenClaw 的设备上访问相同的记忆
4. **Real-time** – WebSocket connection ensures instant synchronization
   **实时** – WebSocket 连接确保即时同步



## Documentation / 文档

- [Installation Guide / 安装指南](plugins/openclaw/INSTALL.md)
- [Troubleshooting / 故障排除](plugins/openclaw/TROUBLESHOOTING.md)
- [Deployment Checklist / 部署检查清单](plugins/openclaw/DEPLOY_CHECKLIST.md)



## License / 许可证

MIT License - see [LICENSE](LICENSE) file for details.

MIT 许可证 – 详情见 [LICENSE](LICENSE) 文件
