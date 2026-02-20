#!/bin/bash
# SoulSync 一键安装脚本
# 用法: curl -sSL https://raw.githubusercontent.com/alanliuc-a11y/soulsync/main/install.sh | bash

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   SoulSync 插件一键安装脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查是否已安装
if [ -d "$HOME/.openclaw/plugins/soulsync" ]; then
    echo -e "${YELLOW}检测到已有 SoulSync 插件，是否覆盖安装？${NC}"
    echo -e "选择覆盖将备份旧版本，并重新配置（需要重新输入邮箱密码）"
    read -p "覆盖安装？(y/n): " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo -e "${RED}安装已取消${NC}"
        exit 0
    fi
    # 备份旧插件（带时间戳）
    BACKUP_DIR="$HOME/.openclaw/plugins/soulsync_backup_$(date +%Y%m%d%H%M%S)"
    echo -e "${YELLOW}正在备份旧插件到 $BACKUP_DIR${NC}"
    mv "$HOME/.openclaw/plugins/soulsync" "$BACKUP_DIR"
    echo -e "${GREEN}备份完成${NC}"
fi

# 创建插件目录
mkdir -p "$HOME/.openclaw/plugins"
cd "$HOME/.openclaw/plugins"

# 克隆最新代码（请替换为你的仓库地址）
echo -e "${GREEN}正在下载 SoulSync 插件...${NC}"
git clone https://github.com/alanliuc-a11y/soulsync.git
cd soulsync

# 进入插件子目录
cd plugins/openclaw

# 创建虚拟环境并安装依赖
echo -e "${GREEN}正在安装 Python 依赖...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 提示用户输入邮箱和密码
echo -e "${GREEN}请输入你的 SoulSync 账户信息（用于登录云端）${NC}"
read -p "邮箱: " EMAIL
read -sp "密码: " PASSWORD
echo ""

# 生成配置文件
cat > config.json <<EOF
{
  "cloud_url": "http://47.96.170.74:3000",
  "email": "$EMAIL",
  "password": "$PASSWORD",
  "workspace": "$HOME/.openclaw/workspace",
  "watch_files": [
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "AGENTS.md",
    "TOOLS.md",
    "skills.json",
    "skills/"
  ]
}
EOF

# 创建监控脚本目录
mkdir -p "$HOME/.openclaw/scripts"

# 创建监控脚本（常驻守护）
cat > "$HOME/.openclaw/scripts/ensure_soulsync.sh" <<'EOF'
#!/bin/bash
if ! pgrep -f "python.*src/main.py" > /dev/null; then
    cd "$HOME/.openclaw/plugins/soulsync/plugins/openclaw"
    ./venv/bin/python src/main.py &
    echo "$(date): SoulSync 已重启" >> "$HOME/.openclaw/logs/soulsync_monitor.log"
fi
EOF
chmod +x "$HOME/.openclaw/scripts/ensure_soulsync.sh"

# 添加到 crontab（每5分钟检查一次）
(crontab -l 2>/dev/null | grep -v ensure_soulsync; echo "*/5 * * * * $HOME/.openclaw/scripts/ensure_soulsync.sh") | crontab -

# 立即启动插件
echo -e "${GREEN}正在启动 SoulSync 插件...${NC}"
"$HOME/.openclaw/scripts/ensure_soulsync.sh"

# 等待几秒让插件启动
sleep 3

# 检查是否运行
if pgrep -f "python.*src/main.py" > /dev/null; then
    echo -e "${GREEN}✅ SoulSync 插件安装成功并已运行！${NC}"
else
    echo -e "${RED}❌ 插件启动失败，请检查日志：$HOME/.openclaw/logs/soulsync_monitor.log${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}安装完成！现在你的 OpenClaw 已拥有灵魂同步能力。${NC}"
echo -e "${GREEN}如有问题，请访问 https://github.com/alanliuc-a11y/soulsync/issues${NC}"