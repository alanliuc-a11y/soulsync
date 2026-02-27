# SoulSync OpenClaw 插件部署检查清单

## 本地 Ubuntu 部署步骤

### ✅ 第1步：准备环境
- [ ] Ubuntu 系统已更新: `sudo apt-get update`
- [ ] Python 3.7+ 已安装: `python3 --version`
- [ ] pip3 已安装: `pip3 --version`

### ✅ 第2步：复制插件文件
```bash
# 创建插件目录
mkdir -p ~/.openclaw/plugins/soulsync

# 复制文件（根据你的实际路径调整）
cp -r /path/to/soulsync/plugins/openclaw/* ~/.openclaw/plugins/soulsync/
```

### ✅ 第3步：安装依赖
```bash
cd ~/.openclaw/plugins/soulsync
pip3 install -r requirements.txt --user
```

### ✅ 第4步：配置插件
```bash
# 编辑配置文件
nano ~/.openclaw/plugins/soulsync/config.json
```

填写以下信息:
```json
{
  "cloud_url": "http://你的服务器IP:3000",
  "email": "你的邮箱",
  "password": "你的密码",
  "workspace": "./workspace",
  "watch_files": ["MEMORY.md", "memory/"]
}
```

### ✅ 第5步：运行诊断
```bash
cd ~/.openclaw/plugins/soulsync
python3 debug.py
```

**期望结果**: 所有检查项显示 ✅

### ✅ 第6步：测试运行
```bash
python3 src/main_fixed.py
```

**期望结果**:
- 成功加载配置
- 成功连接服务器（如果配置了账号）
- 文件监听器启动
- 显示 "Plugin Running"

### ✅ 第7步：集成到 OpenClaw
1. 确保 `openclaw.plugin.json` 格式正确
2. 重启 OpenClaw
3. 在 OpenClaw 中启用 SoulSync 插件

---

## 常见问题速查

| 问题 | 快速解决 |
|------|---------|
| ModuleNotFoundError | `export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"` |
| Permission Denied | `chmod -R 755 ~/.openclaw/plugins/soulsync` |
| 依赖安装失败 | `sudo apt-get install python3-dev` |
| WebSocket 失败 | 检查 config.json 中的 cloud_url |
| 文件监听失败 | `echo fs.inotify.max_user_watches=524288 \| sudo tee -a /etc/sysctl.conf && sudo sysctl -p` |

---

## 验证部署成功

运行以下命令验证:
```bash
cd ~/.openclaw/plugins/soulsync

# 1. 检查文件结构
ls -la

# 2. 检查依赖
pip3 list | grep -E "requests|watchdog|websocket"

# 3. 运行诊断
python3 debug.py

# 4. 测试启动（按 Ctrl+C 退出）
python3 src/main_fixed.py
```

---

## 同步到 GitHub

调试完成后，提交到 GitHub:

```bash
cd /path/to/soulsync

# 查看修改的文件
git status

# 添加新文件
git add plugins/openclaw/debug.py
git add plugins/openclaw/setup.sh
git add plugins/openclaw/INSTALL.md
git add plugins/openclaw/TROUBLESHOOTING.md
git add plugins/openclaw/src/__init__.py
git add plugins/openclaw/src/main_fixed.py
git add plugins/openclaw/DEPLOY_CHECKLIST.md

# 提交修改
git commit -m "fix: 修复 Ubuntu 安装问题

- 添加 __init__.py 解决 Python 模块导入问题
- 创建 main_fixed.py 修复跨平台路径问题
- 添加 debug.py 诊断工具
- 添加 setup.sh 自动安装脚本
- 添加完整文档（INSTALL, TROUBLESHOOTING, DEPLOY_CHECKLIST）
- 更新版本号到 1.0.2"

# 推送到 GitHub
git push origin main
```

---

## NPM 发布（如果适用）

```bash
cd plugins/openclaw

# 更新版本号
npm version patch  # 或 minor/major

# 发布到 NPM
npm publish
```

---

**最后更新**: 2026-02-26
**版本**: 1.0.2
