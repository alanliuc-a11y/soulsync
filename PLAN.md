# SoulSync 开发规划 (v2)

## 项目概述
- **项目名称**: SoulSync - 跨机器人的云端记忆同步服务
- **核心功能**: 云端存储用户记忆，支持实时同步，通过 OpenClaw 插件实现本地文件与云端的双向同步
- **技术栈**:
  - 云端: Node.js + Express + SQLite + WebSocket (ws)
  - 插件: Python (watchdog + requests)

---

## 第一阶段开发任务

### 1. 项目结构搭建

```
soulsync/
├── server/                    # 云端服务
│   ├── src/
│   │   ├── index.js          # 入口文件
│   │   ├── database.js       # SQLite 数据库操作
│   │   ├── middleware/
│   │   │   └── auth.js       # 认证中间件
│   │   │   └── subscription.js # 付费订阅中间件
│   │   ├── routes/
│   │   │   ├── auth.js       # 注册/登录 API
│   │   │   └── memories.js  # 记忆 CRUD API
│   │   ├── websocket.js      # WebSocket 管理
│   │   └── sync.js           # 同步逻辑
│   ├── package.json
│   └── soulsync.db           # SQLite 数据库文件
│
├── plugins/                   # 插件目录
│   ├── base/                  # 插件基类 (便于扩展 CoPaw)
│   │   ├── __init__.py
│   │   ├── client.py          # API/WS 客户端基类
│   │   ├── watcher.py         # 文件监听基类
│   │   ├── sync.py            # 同步基类
│   │   └── format_converter.py # 格式转换接口 (预留)
│   │
│   └── openclaw/             # OpenClaw 插件
│       ├── src/
│       │   ├── watcher.py    # 文件监听实现
│       │   ├── sync.py       # 同步实现
│       │   ├── client.py    # API/WS 客户端实现
│       │   └── main.py       # 入口
│       ├── config.json       # 配置文件 (只需邮箱)
│       ├── requirements.txt  # Python 依赖
│       └── workspace/        # 工作目录
│           └── MEMORY.md     # 记忆文件
│
└── README.md                 # 项目说明
```

---

### 2. 云端服务开发 (server/)

#### 2.1 数据库设计

**users 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 用户ID |
| device_id | TEXT UNIQUE | 设备ID (插件自动生成) |
| email | TEXT UNIQUE | 用户邮箱 |
| password | TEXT | 密码 (明文) |
| subscription_status | TEXT | 订阅状态: 'trial'(试用), 'active'(付费), 'expired'(过期) |
| trial_start_date | DATETIME | 试用开始日期 |
| subscription_expire_date | DATETIME | 订阅到期日期 (试用为7天后) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**memories 表**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 记忆ID |
| user_id | INTEGER | 所属用户ID |
| content | TEXT | 记忆完整内容 (整个 MEMORY.md) |
| version | INTEGER | 版本号 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**connections 表 (WebSocket)**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 连接ID |
| user_id | INTEGER | 关联用户ID |
| socket_id | TEXT | WebSocket ID |

---

#### 2.2 API 接口

| 方法 | 路径 | 说明 | 认证 | 付费 |
|------|------|------|------|------|
| POST | /api/auth/register | 注册 (设备ID+邮箱+密码) | 否 | - |
| POST | /api/auth/login | 登录 (邮箱+密码) | 否 | - |
| POST | /api/auth/device | 设备注册/登录 (自动注册) | 设备ID | - |
| GET | /api/memories | 获取用户记忆 | 是 | - |
| POST | /api/memories | 上传/覆盖记忆 | 是 | 是 |
| GET | /api/memories/sync?version={version} | 增量同步 | 是 | 是 |
| GET | /api/user/profile | 获取用户信息 | 是 | - |
| POST | /api/user/bind-email | 绑定邮箱 (多设备同步) | 是 | - |

**认证方式**: Header 中携带 `Authorization: Bearer {token}` (token = user_id:session_token)

---

#### 2.3 付费订阅中间件

- 新用户注册时自动设置为 'trial' 状态，试用7天
- 中间件检查 `subscription_status`:
  - 'trial': 检查是否在7天内，是则允许，否则拒绝
  - 'active': 检查是否在订阅期内，是则允许，否则拒绝
  - 'expired': 直接拒绝

---

#### 2.4 WebSocket 事件

| 事件名 | 方向 | 说明 |
|--------|------|------|
| connect | Client → Server | 客户端连接时发送 token |
| new_memory | Server → Client | 有新记忆时广播给用户 |
| sync_update | Server → Client | 推送增量更新 |

---

### 3. OpenClaw 插件开发 (plugins/openclaw/)

#### 3.1 配置文件 (config.json)
```json
{
  "cloud_url": "https://your-cloud-server.com",
  "email": "user@example.com",
  "password": "user_password",
  "workspace": "./workspace",
  "memory_file": "MEMORY.md"
}
```

**注意**: 插件不硬编码服务器地址，用户配置 `cloud_url`

#### 3.2 核心功能

1. **自动注册/登录** (client.py)
   - 启动时检查本地是否有 token
   - 若无 token，使用设备ID自动注册或登录
   - 登录成功后保存 token 到本地

2. **设备ID管理** (main.py)
   - 首次运行时生成唯一设备ID (UUID)
   - 保存到 `config.json` 或独立 `device_id` 文件
   - 用设备ID作为用户标识进行注册/登录

3. **文件监听** (watcher.py)
   - 使用 watchdog 监听 workspace/MEMORY.md 变化
   - 检测到变化时触发完整上传

4. **同步逻辑** (sync.py)
   - 启动时从云端下载整个记忆文件，写入本地 MEMORY.md
   - 本地文件变化时上传整个内容覆盖云端
   - 简化版增量同步：每次全量上传/下载

5. **WebSocket 客户端** (client.py)
   - 连接云端 WebSocket
   - 接收 new_memory 事件
   - 收到通知后拉取更新并写入本地

---

### 4. 插件基类设计 (plugins/base/)

```python
# plugins/base/format_converter.py (预留接口)
class FormatConverter:
    """格式转换基类 - 预留接口"""
    
    @staticmethod
    def to_cloud(local_content: str, source_type: str) -> str:
        """本地格式转换为云端格式"""
        raise NotImplementedError
    
    @staticmethod
    def from_cloud(cloud_content: str, target_type: str) -> str:
        """云端格式转换为本 地格式"""
        raise NotImplementedError

# plugins/base/client.py
class BaseClient:
    """API/WS 客户端基类"""
    
    def __init__(self, config: dict):
        self.config = config
        self.token = None
    
    def register_or_login(self, device_id: str) -> dict:
        """自动注册/登录"""
        raise NotImplementedError
    
    def upload_memory(self, content: str) -> dict:
        """上传记忆"""
        raise NotImplementedError
    
    def download_memory(self) -> str:
        """下载记忆"""
        raise NotImplementedError

# plugins/base/watcher.py
class BaseWatcher:
    """文件监听基类"""
    
    def __init__(self, path: str, callback):
        self.path = path
        self.callback = callback
    
    def start(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
```

---

### 5. 测试方法

#### 测试1: 云端服务
```bash
cd server
npm install
node src/index.js
# 访问 http://localhost:3000/api/health
```

#### 测试2: 注册/登录 + 设备自动注册
```bash
# 方式1: 设备自动注册 (插件首次运行)
curl -X POST http://localhost:3000/api/auth/device \
  -H "Content-Type: application/json" \
  -d '{"device_id":"生成的UUID","email":"test@example.com","password":"123456"}'

# 方式2: 手动注册
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"device_id":"uuid-123","email":"test@example.com","password":"123456"}'
```

#### 测试3: 插件同步
- 修改 config.json 中的 cloud_url 为实际服务器地址
- 启动插件 A，修改 MEMORY.md，观察上传
- 启动插件 B，验证能收到 WebSocket 通知并同步
- 检查两边的 MEMORY.md 内容一致

#### 测试4: 付费订阅
- 检查新用户 trial_status = 'trial', 7天后过期
- 调用同步接口应该成功
- 7天后调用同步接口应该被拒绝

---

## 开发顺序

1. **云端服务** (server/)
   - [ ] 创建 package.json，安装依赖
   - [ ] 实现 database.js (建表、CRUD)
   - [ ] 实现 middleware/auth.js (认证)
   - [ ] 实现 middleware/subscription.js (付费中间件)
   - [ ] 实现 routes/auth.js (注册/登录/设备注册 API)
   - [ ] 实现 routes/memories.js (记忆 CRUD + 简化同步)
   - [ ] 实现 websocket.js (实时通知)
   - [ ] 实现 index.js (入口)

2. **插件基类** (plugins/base/)
   - [ ] 创建 __init__.py
   - [ ] 实现 format_converter.py (预留)
   - [ ] 实现 client.py (基类)
   - [ ] 实现 watcher.py (基类)
   - [ ] 实现 sync.py (基类)

3. **OpenClaw 插件** (plugins/openclaw/)
   - [ ] 创建目录结构
   - [ ] 创建 config.json
   - [ ] 创建 requirements.txt
   - [ ] 实现 client.py (继承基类)
   - [ ] 实现 watcher.py (继承基类)
   - [ ] 实现 sync.py (继承基类)
   - [ ] 实现 main.py (入口 + 设备ID管理)

4. **测试与文档**
   - [ ] 编写运行测试说明

---

## 注意事项

- **安全性简化**: 密码暂不加密，token 使用简化实现
- **同步简化**: 每次上传/下载整个 MEMORY.md 文件
- **设备ID**: 首次运行自动生成 UUID 作为设备ID
- **多设备绑定**: 预留接口，初期单设备测试
- **格式转换**: 基类预留接口，OpenClaw 直接读写
