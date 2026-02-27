# SoulSync OpenClaw 插件安装指南

## Ubuntu/Linux 安装步骤

### 1. 安装系统依赖
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
```

### 2. 安装 Python 依赖
```bash
cd /path/to/openclaw/plugins/soulsync
pip3 install -r requirements.txt
```

### 3. 配置文件
复制配置模板并修改：
```bash
cp config.json config.json.backup
```

编辑 `config.json`：
```json
{
  "cloud_url": "http://你的服务器IP:3000",
  "email": "你的邮箱",
  "password": "你的密码",
  "workspace": "./workspace",
  "memory_file": "MEMORY.md",
  "watch_files": [
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "AGENTS.md",
    "TOOLS.md",
    "skills.json",
    "memory/",
    "MEMORY.md"
  ]
}
```

### 4. 创建工作目录
```bash
mkdir -p workspace/memory
```

### 5. 测试运行
```bash
python3 src/main.py
```

## 常见问题排查

### 问题1：ModuleNotFoundError
**错误**：`No module named 'src'`

**解决**：
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题2：Permission Denied
**错误**：无法写入文件

**解决**：
```bash
chmod -R 755 /path/to/plugin
```

### 问题3：Watchdog 错误
**错误**：`inotify` 限制

**解决**：
```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 调试模式

启用详细日志：
```bash
DEBUG=1 python3 src/main.py
```

## 手动安装到 OpenClaw

1. 找到 OpenClaw 插件目录：
   ```bash
   # 通常在用户目录下
   ~/.openclaw/plugins/
   # 或
   /usr/share/openclaw/plugins/
   ```

2. 复制插件：
   ```bash
   cp -r /path/to/soulsync/plugins/openclaw ~/.openclaw/plugins/
   ```

3. 重启 OpenClaw
