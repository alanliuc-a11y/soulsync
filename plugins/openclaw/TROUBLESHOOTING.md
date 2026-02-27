# SoulSync OpenClaw 插件故障排除指南

## 常见问题及解决方案

### 1. 安装时提示 "No module named 'src'"

**原因**: Python 路径问题

**解决**:
```bash
# 方法1: 在插件目录运行
cd /path/to/openclaw/plugins/soulsync
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python3 src/main.py

# 方法2: 使用修复版 main_fixed.py
python3 src/main_fixed.py
```

### 2. OpenClaw 无法识别插件

**原因**: 插件目录结构不正确

**解决**:
```bash
# 检查插件目录结构
ls -la ~/.openclaw/plugins/soulsync/

# 应该包含:
# - openclaw.plugin.json
# - src/
# - config.json

# 如果结构不对，重新复制
cp -r /path/to/soulsync/plugins/openclaw ~/.openclaw/plugins/soulsync
```

### 3. watchdog 安装失败

**原因**: 缺少系统依赖

**解决**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip

# 然后重新安装
pip3 install watchdog --user
```

### 4. 权限错误 Permission Denied

**解决**:
```bash
# 修复权限
chmod -R 755 ~/.openclaw/plugins/soulsync

# 确保当前用户有写入权限
sudo chown -R $(whoami):$(whoami) ~/.openclaw/plugins/soulsync
```

### 5. WebSocket 连接失败

**原因**: 服务器地址配置错误或网络问题

**解决**:
```bash
# 检查 config.json
cat ~/.openclaw/plugins/soulsync/config.json

# 测试服务器连通性
curl http://your-server:3000/health

# 检查防火墙
sudo ufw status
```

### 6. 文件监听不工作 (inotify 限制)

**解决**:
```bash
# 增加 inotify 限制
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# 验证
cat /proc/sys/fs/inotify/max_user_watches
```

### 7. Python 版本过低

**检查**:
```bash
python3 --version  # 需要 >= 3.7

# 如果版本过低，安装新版本
sudo apt-get install python3.8 python3.8-pip
```

## 调试步骤

### Step 1: 运行诊断脚本
```bash
cd ~/.openclaw/plugins/soulsync
python3 debug.py
```

### Step 2: 检查日志
```bash
# 如果有日志文件
tail -f ~/.openclaw/logs/soulsync.log

# 或者直接运行看输出
python3 src/main_fixed.py 2>&1 | tee debug.log
```

### Step 3: 手动测试组件
```bash
# 测试客户端
python3 -c "from src.client import OpenClawClient; print('Client OK')"

# 测试监听器
python3 -c "from src.watcher import OpenClawMultiWatcher; print('Watcher OK')"
```

## OpenClaw 特定问题

### OpenClaw 插件加载失败

1. **检查插件格式**:
```bash
cat ~/.openclaw/plugins/soulsync/openclaw.plugin.json
```

2. **验证 JSON 格式**:
```bash
python3 -m json.tool ~/.openclaw/plugins/soulsync/openclaw.plugin.json
```

3. **重启 OpenClaw**:
```bash
# 找到 OpenClaw 进程并重启
pkill -f openclaw
# 然后重新启动 OpenClaw
```

### 插件版本不匹配

检查 OpenClaw 版本:
```bash
openclaw --version
```

查看插件兼容性:
```bash
cat ~/.openclaw/plugins/soulsync/openclaw.plugin.json | grep version
```

## 获取帮助

如果以上方法都无法解决问题:

1. 运行诊断脚本并保存输出:
```bash
python3 debug.py > diagnostic.log 2>&1
```

2. 收集以下信息:
   - OpenClaw 版本
   - Python 版本: `python3 --version`
   - 操作系统: `uname -a`
   - 插件目录结构: `tree ~/.openclaw/plugins/soulsync`
   - 错误日志

3. 提交 Issue 到 GitHub:
https://github.com/alanliuc-a11y/soulsync/issues

## 快速修复命令

一键修复常见问题:
```bash
cd ~/.openclaw/plugins/soulsync

# 修复权限
chmod -R 755 .

# 安装依赖
pip3 install -r requirements.txt --user

# 创建工作目录
mkdir -p workspace/memory

# 运行诊断
python3 debug.py

# 启动插件
python3 src/main_fixed.py
```
