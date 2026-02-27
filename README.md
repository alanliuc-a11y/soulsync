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

- **Subscription model** – Free tier + paid tiers with yearly discount.  
  **订阅模式** – 免费版 + 付费版，年付享优惠。

- **Progressive open source** – Backend code will be open-sourced after each major phase.  
  **渐进式开源** – 后端代码将在每个大阶段完成后开源。



## Backend Service / 后端服务

The backend service is officially hosted and maintained by the SoulSync team. Users only need to install the plugin and connect to the official cloud service.

后端服务由 SoulSync 团队官方托管和维护。用户只需安装插件，连接官方云服务即可。

**Current Phase / 当前阶段**: Phase 1 - Basic sync (v1.0.x)

**Pricing / 定价**:

| Tier / 层级 | Monthly / 月付 | Yearly / 年付 | Files / 同步文件 |
|-------------|----------------|---------------|------------------|
| **Free / 免费** | $0 | - | MEMORY.md, USER.md |
| **Basic / 初级** | $1.19 / ¥4.9 | $11.9 / ¥49 | + IDENTITY.md, SOUL.md, TOOLS.md |
| **Pro / 高级** | $3.99 / ¥12.9 | $39.9 / ¥129 | + AGENTS.md, skills.json, memory/ |

- Free tier provides essential emotional connection - your bot remembers your name and preferences immediately
- 免费版提供核心的情感连接 - 你的机器人立即记得你的名字和偏好
- Upgrade anytime to unlock more files
- 随时升级解锁更多文件



## Open Source Roadmap / 开源路线图

SoulSync follows a **5-phase progressive open-source strategy**. After each phase, the previous phase's backend code will be open-sourced.

SoulSync 采用**五阶段渐进式开源策略**。每个阶段完成后，前一阶段的后端代码将开源。

| Phase | Version | Features | Open Source Timeline |
|-------|---------|----------|---------------------|
| **Phase 1** | v1.0.x | Basic sync, single user | After Phase 2 release |
| **Phase 2** | v2.0.0 | Multi-bot collaboration | After Phase 3 release |
| **Phase 3** | v3.0.0 | "Singularity" | After Phase 4 release |
| **Phase 4** | v4.0.0 | "Fusion" | After Phase 5 release |
| **Phase 5** | v5.0.0 | "Evolution" | Fully open source |

This approach ensures:
- ✅ Sustainable development with subscription revenue
- ✅ Community trust through progressive transparency
- ✅ Self-hosting option for users who need it
- ✅ Continuous innovation and feature development

这种策略确保：
- ✅ 通过订阅收入维持可持续开发
- ✅ 通过渐进式透明建立社区信任
- ✅ 为需要自托管的用户提供选择
- ✅ 持续创新和功能开发



## Features Detail / 功能详情

- **Lightweight & easy to deploy** – Node.js backend + SQLite database.  
  **轻量易部署** – Node.js 后端 + SQLite 数据库。



## Project Structure / 项目结构

```
soulsync/
├── plugins/
│   ├── base/            # Base classes for future bots
│   └── openclaw/        # OpenClaw plugin (this repo)
│       ├── src/
│       ├── config.json.example
│       └── requirements.txt
└── README.md

Note: Backend server code is maintained separately and will be open-sourced progressively according to our roadmap.
注意：后端服务代码单独维护，将根据路线图逐步开源。
```



## Getting Started / 快速开始



### 1. Register account / 注册账号

Visit our official website (coming soon) to register an account and start your 7-day free trial.

访问我们的官方网站（即将上线）注册账号，开始 7 天免费试用。



### 2. Install the OpenClaw plugin / 安装 OpenClaw 插件



### 3. Configure the plugin / 配置插件

Edit `~/.openclaw/extensions/soulsync/config.json`:

编辑 `~/.openclaw/extensions/soulsync/config.json`：

```json
{
  "cloud_url": "http://official-server.soulsync.io:3000",
  "email": "your-email@example.com",
  "password": "your-password"
}
```

Note: The cloud_url points to the official SoulSync server. Self-hosting will be available after the corresponding phase is open-sourced.

注意：cloud_url 指向官方 SoulSync 服务器。自托管将在对应阶段开源后可用。



### 4. Start the plugin / 启动插件

```bash
openclaw soulsync:start
```



## Self-Hosting (Future) / 自托管（未来）

According to our [Open Source Roadmap](#open-source-roadmap--开源路线图), backend code will be progressively open-sourced:

根据我们的[开源路线图](#open-source-roadmap--开源路线图)，后端代码将逐步开源：

- **Phase 1 code**: Available after v2.0.0 release (estimated Q3 2026)
- **Phase 2 code**: Available after v3.0.0 release (estimated Q1 2027)
- **Phase 3 code**: Available after v4.0.0 release (estimated Q3 2027)
- **Phase 4 code**: Available after v5.0.0 release (estimated 2028)
- **Phase 5 code**: Fully open source

If you need self-hosting immediately, please consider:
- Supporting the project through subscription
- Contributing to the plugin development
- Waiting for the corresponding phase release

如果您需要立即自托管，请考虑：
- 通过订阅支持项目
- 参与插件开发
- 等待对应阶段发布



## How It Works / 工作原理

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
