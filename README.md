\# SoulSync



\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



SoulSync is a \*\*cross-bot soul synchronization system\*\*. It allows your AI assistants (like OpenClaw) to share the same memory, personality, and skills across multiple devices and platforms.  

SoulSync 是一个\*\*跨机器人灵魂同步系统\*\*，让你的 AI 助理（如 OpenClaw）在多设备、多平台之间共享相同的记忆、人格和技能。



\## Features / 功能特性



\- \*\*Cloud-based memory storage\*\* – All memories are stored in the cloud, accessible from anywhere.  

&nbsp; \*\*云端记忆存储\*\* – 所有记忆都存储在云端，随时随地可访问。

\- \*\*Real-time synchronization\*\* – Changes are instantly synced via WebSocket.  

&nbsp; \*\*实时同步\*\* – 通过 WebSocket 实现即时同步。

\- \*\*Multi-bot support\*\* – Currently supports OpenClaw; more bots (CoPaw, etc.) coming soon.  

&nbsp; \*\*多机器人支持\*\* – 目前已支持 OpenClaw，后续将支持 CoPaw 等更多机器人。

\- \*\*Subscription model\*\* – 7-day free trial, then $1/month.  

&nbsp; \*\*订阅模式\*\* – 7 天免费试用，之后每月 1 美元。

\- \*\*Lightweight \& easy to deploy\*\* – Node.js backend + SQLite database.  

&nbsp; \*\*轻量易部署\*\* – Node.js 后端 + SQLite 数据库。



\## Project Structure / 项目结构

soulsync/

├── server/ # Node.js backend

│ ├── src/

│ ├── package.json

│ └── soulsync.db # SQLite database (ignored by git)

├── plugins/

│ ├── base/ # Base classes for future bots

│ └── openclaw/ # OpenClaw plugin

│ ├── src/

│ ├── config.json.example

│ └── requirements.txt

└── README.md



\## Getting Started / 快速开始



\### 1. Deploy the backend / 部署后端



On your cloud server (e.g., Aliyun ECS), run:



```bash

cd server

npm install

node src/index.js



For production, use PM2:

npm install -g pm2

pm2 start src/index.js --name soulsync

pm2 save

pm2 startup



Make sure port 3000 is open in your firewall / security group.



2\. Install the OpenClaw plugin / 安装 OpenClaw 插件

On your OpenClaw machine, copy the plugins/openclaw folder to OpenClaw's plugin directory (e.g., ~/.openclaw/plugins/soulsync). Then install dependencies and configure:



2\. Install the OpenClaw plugin / 安装 OpenClaw 插件

On your OpenClaw machine, copy the plugins/openclaw folder to OpenClaw's plugin directory (e.g., ~/.openclaw/plugins/soulsync). Then install dependencies and configure:



cd ~/.openclaw/plugins/soulsync

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt



Edit config.json (copy from config.json.example):



{

&nbsp; "cloud\_url": "http://your-server-ip:3000",

&nbsp; "email": "your-email@example.com",

&nbsp; "password": "your-password",

&nbsp; "workspace": "/home/your-username/.openclaw/workspace",

&nbsp; "memory\_file": "MEMORY.md"

}



To keep the plugin running, use the provided monitor script:



~/openclaw/scripts/ensure\_soulsync.sh



(You can set up a cron job to run it every 5 minutes.)



3\. Test the sync / 测试同步

Modify MEMORY.md in OpenClaw's workspace.



Check the plugin logs – you should see upload messages.



On your server, query the database to verify:





cd /root/server

sqlite3 soulsync.db "SELECT content FROM memories ORDER BY id DESC LIMIT 1;"





Supported Files (Current) / 当前支持的文件

MEMORY.md



memory/ directory (daily notes)



Future versions will sync personality files (SOUL.md, IDENTITY.md, etc.), skills, and configurations.



Roadmap / 开发计划

Memory sync for OpenClaw



Personality files sync (SOUL.md, IDENTITY.md, USER.md)



Configuration sync (openclaw.json, AGENTS.md, TOOLS.md)



Skills and settings sync



CoPaw plugin



End-to-end encryption for sensitive data



Contributing / 贡献指南

Contributions are welcome! Feel free to open issues or pull requests.

欢迎贡献代码！欢迎提交 issue 或 pull request。



License / 许可证

MIT © Alan Liu

