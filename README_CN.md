# SoulSync

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SoulSync 是一个**跨机器人灵魂同步系统**，让你的 AI 助理（如 OpenClaw）在多设备、多平台之间共享相同的记忆、人格和技能。

## 功能特性

- **云端记忆存储** – 所有记忆都存储在云端，随时随地可访问
- **实时同步** – 通过 WebSocket 实现即时同步
- **多机器人支持** – 目前已支持 OpenClaw，后续将支持 CoPaw 等更多机器人
- **订阅模式** – 7 天免费试用，之后每月 1 美元
- **轻量易部署** – Node.js 后端 + SQLite 数据库

## 项目结构

```
soulsync/
├── server/              # Node.js 后端
│   ├── src/
│   ├── package.json
│   └── soulsync.db      # SQLite 数据库（git 忽略）
├── plugins/
│   ├── base/            # 基础类（供后续机器人使用）
│   └── openclaw/        # OpenClaw 插件
│       ├── src/
│       ├── config.json.example
│       └── requirements.txt
└── README.md
```

## 快速开始

### 1. 部署后端

在你的云服务器（如阿里云 ECS）上运行：

```bash
cd server
npm install
node src/index.js
```

生产环境建议使用 PM2：

```bash
npm install -g pm2
pm2 start src/index.js --name soulsync
pm2 save
pm2 startup
```

确保防火墙/安全组中已开放 3000 端口。

### 2. 安装 OpenClaw 插件

```bash
openclaw plugins install soulsync
```

或从本地目录安装：

```bash
openclaw plugins install /path/to/soulsync/plugins/openclaw
```

### 3. 配置插件

编辑 `~/.openclaw/extensions/soulsync/config.json`：

```json
{
  "cloud_url": "http://your-server:3000",
  "email": "your-email@example.com",
  "password": "your-password"
}
```

### 4. 启动插件

```bash
openclaw soulsync:start
```

## 工作原理

SoulSync 为你的 AI 助理创建了一个持久化的记忆层：

1. **记忆文件** – 将机器人的身份、技能和记忆存储在 Markdown 文件中
2. **云端同步** – 所有更改自动上传到云端
3. **多设备** – 在任何安装了 OpenClaw 的设备上访问相同的记忆
4. **实时** – WebSocket 连接确保即时同步

## 文档

- [安装指南](plugins/openclaw/INSTALL.md)
- [故障排除](plugins/openclaw/TROUBLESHOOTING.md)
- [部署检查清单](plugins/openclaw/DEPLOY_CHECKLIST.md)

## 许可证

MIT 许可证 – 详情见 [LICENSE](LICENSE) 文件
