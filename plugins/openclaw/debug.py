#!/usr/bin/env python3
"""
SoulSync OpenClaw 插件调试工具
用于检查安装环境和依赖
"""

import sys
import os
import json
import importlib.util

def check_python_version():
    """检查 Python 版本"""
    print("=" * 50)
    print("Python 版本检查")
    print("=" * 50)
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 需要 Python 3.7 或更高版本")
        return False
    print("✅ Python 版本符合要求")
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n" + "=" * 50)
    print("依赖包检查")
    print("=" * 50)
    
    required = {
        'requests': 'requests>=2.28.0',
        'watchdog': 'watchdog>=3.0.0',
        'websocket': 'websocket-client>=1.6.0'
    }
    
    all_ok = True
    for module, package in required.items():
        try:
            if module == 'websocket':
                importlib.import_module('websocket')
            else:
                importlib.import_module(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            all_ok = False
    
    return all_ok

def check_file_structure():
    """检查文件结构"""
    print("\n" + "=" * 50)
    print("文件结构检查")
    print("=" * 50)
    
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"插件目录: {plugin_dir}")
    
    required_files = [
        'openclaw.plugin.json',
        'config.json',
        'requirements.txt',
        'src/main.py',
        'src/__init__.py',
        'src/client.py',
        'src/watcher.py',
        'src/sync.py',
    ]
    
    all_ok = True
    for file in required_files:
        path = os.path.join(plugin_dir, file)
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
        if not exists:
            all_ok = False
    
    return all_ok

def check_config():
    """检查配置文件"""
    print("\n" + "=" * 50)
    print("配置文件检查")
    print("=" * 50)
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    if not os.path.exists(config_path):
        print("❌ config.json 不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ config.json 格式正确")
        
        # 检查必要字段
        required_fields = ['cloud_url', 'email', 'password', 'workspace']
        for field in required_fields:
            value = config.get(field)
            if value:
                if field in ['email', 'password']:
                    print(f"✅ {field}: {'*' * len(str(value))}")
                else:
                    print(f"✅ {field}: {value}")
            else:
                print(f"⚠️  {field}: 未配置")
        
        return True
    except json.JSONDecodeError as e:
        print(f"❌ config.json 格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取 config.json 失败: {e}")
        return False

def check_workspace():
    """检查工作目录"""
    print("\n" + "=" * 50)
    print("工作目录检查")
    print("=" * 50)
    
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    workspace = os.path.join(plugin_dir, 'workspace')
    
    if os.path.exists(workspace):
        print(f"✅ workspace 目录存在: {workspace}")
        
        # 检查是否可写
        if os.access(workspace, os.W_OK):
            print("✅ workspace 目录可写")
        else:
            print("❌ workspace 目录不可写")
            return False
    else:
        print(f"⚠️  workspace 目录不存在: {workspace}")
        try:
            os.makedirs(workspace, exist_ok=True)
            print("✅ 已创建 workspace 目录")
        except Exception as e:
            print(f"❌ 创建 workspace 目录失败: {e}")
            return False
    
    return True

def test_import():
    """测试导入主模块"""
    print("\n" + "=" * 50)
    print("模块导入测试")
    print("=" * 50)
    
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(plugin_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    try:
        from main import SoulSyncPlugin
        print("✅ 成功导入 SoulSyncPlugin")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("SoulSync OpenClaw 插件调试工具")
    print("=" * 50 + "\n")
    
    checks = [
        ("Python 版本", check_python_version),
        ("依赖包", check_dependencies),
        ("文件结构", check_file_structure),
        ("配置文件", check_config),
        ("工作目录", check_workspace),
        ("模块导入", test_import),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 检查出错: {e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("检查结果总结")
    print("=" * 50)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！插件应该可以正常运行。")
        print("\n运行命令: python3 src/main.py")
    else:
        print("⚠️  部分检查未通过，请根据上方提示修复问题。")
        print("\n常见问题解决:")
        print("1. 安装依赖: pip3 install -r requirements.txt")
        print("2. 修复权限: chmod -R 755 .")
        print("3. 创建目录: mkdir -p workspace/memory")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
