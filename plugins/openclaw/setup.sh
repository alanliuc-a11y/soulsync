#!/bin/bash
# SoulSync OpenClaw 插件 Linux 安装脚本

set -e  # 遇到错误立即退出

echo "======================================"
echo "SoulSync OpenClaw 插件安装脚本"
echo "======================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "插件目录: $SCRIPT_DIR"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3"
    echo "请安装 Python3: sudo apt-get install python3"
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip3"
    echo "请安装 pip3: sudo apt-get install python3-pip"
    exit 1
fi

echo "✅ pip3 已安装"

# 安装依赖
echo ""
echo "正在安装 Python 依赖..."
pip3 install -r requirements.txt --user

echo "✅ 依赖安装完成"

# 创建必要的目录
echo ""
echo "创建工作目录..."
mkdir -p workspace/memory
echo "✅ 工作目录创建完成"

# 检查配置文件
echo ""
if [ ! -f "config.json" ]; then
    echo "⚠️  config.json 不存在"
    if [ -f "config.json.example" ]; then
        cp config.json.example config.json
        echo "✅ 已从模板创建 config.json"
        echo "⚠️  请编辑 config.json 配置你的账号信息"
    else
        echo "❌ 未找到配置文件模板"
        exit 1
    fi
else
    echo "✅ config.json 已存在"
fi

# 检查权限
echo ""
echo "检查文件权限..."
chmod -R 755 "$SCRIPT_DIR"
chmod +x debug.py
if [ -f "setup.sh" ]; then
    chmod +x setup.sh
fi
echo "✅ 权限设置完成"

# 运行调试检查
echo ""
echo "运行安装检查..."
python3 debug.py

echo ""
echo "======================================"
echo "安装完成！"
echo "======================================"
echo ""
echo "使用方法:"
echo "1. 编辑 config.json 配置你的账号"
echo "2. 运行插件: python3 src/main.py"
echo "3. 或使用修复版: python3 src/main_fixed.py"
echo ""
echo "调试命令: python3 debug.py"
echo ""
