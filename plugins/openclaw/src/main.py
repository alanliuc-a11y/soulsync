import json
import os
import sys
import time
import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'base'))

from src.client import OpenClawClient
from src.watcher import OpenClawWatcher
from src.sync import OpenClawSync


class SoulSyncPlugin:
    """SoulSync OpenClaw 插件主类"""
    
    def __init__(self):
        self.config = None
        self.client = None
        self.watcher = None
        self.sync = None
        self.running = False
    
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        workspace = self.config.get('workspace', './workspace')
        workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), workspace))
        
        memory_file = self.config.get('memory_file', 'MEMORY.md')
        self.memory_file_path = os.path.join(workspace, memory_file)
        
        self.config['workspace'] = workspace
        self.config['memory_file_path'] = self.memory_file_path
        
        print(f"Config loaded:")
        print(f"  Cloud URL: {self.config.get('cloud_url')}")
        print(f"  Workspace: {workspace}")
        print(f"  Memory file: {self.memory_file_path}")
    
    def initialize(self):
        """初始化组件"""
        print("\n=== Initializing SoulSync Plugin ===\n")
        
        self.client = OpenClawClient(self.config)
        
        email = self.config.get('email')
        password = self.config.get('password')
        
        if not email or not password:
            print("WARNING: Email and password not configured!")
            print("Please edit config.json and add your email and password\n")
        
        try:
            self.client.authenticate(email, password)
        except Exception as e:
            print(f"Authentication error: {e}")
            print("Please check your config.json and try again\n")
            raise
        
        profile = self.client.get_profile()
        print(f"\nLogged in as: {profile.get('email')}")
        subscription = profile.get('subscription', {})
        print(f"Subscription: {subscription.get('status')} (days remaining: {subscription.get('daysRemaining', 0)})\n")
        
        self.sync = OpenClawSync(self.client, self.watcher)
        self.sync.set_memory_file(self.memory_file_path)
        
        print("Pulling initial memory from cloud...")
        self.sync.pull()
        
        print("\nStarting file watcher...")
        self.watcher = OpenClawWatcher(self.memory_file_path, self.on_file_change)
        self.watcher.start()
        
        print("\nConnecting to WebSocket...")
        self.client.connect_websocket(self.on_websocket_message)
        
        self.running = True
    
    def on_file_change(self, event_type: str, file_path: str = None):
        """文件变化回调"""
        print(f"\n[File {event_type}] {file_path}")
        
        if event_type in ['modified', 'created']:
            time.sleep(0.5)
            
            try:
                self.sync.push()
                print("Upload completed")
            except Exception as e:
                print(f"Upload error: {e}")
    
    def on_websocket_message(self, data: dict):
        """WebSocket 消息回调"""
        event = data.get('event')
        
        if event == 'new_memory':
            print(f"\n[WebSocket] New memory available!")
            try:
                self.sync.pull()
                print("Memory synced from remote")
            except Exception as e:
                print(f"Sync error: {e}")
        elif data.get('type') == 'authenticated':
            print(f"[WebSocket] Authenticated, socket_id: {data.get('socket_id')}")
        elif data.get('type') == 'error':
            print(f"[WebSocket] Error: {data.get('message')}")
    
    def run(self):
        """运行插件"""
        print("\n" + "=" * 50)
        print("SoulSync OpenClaw Plugin")
        print("=" * 50 + "\n")
        
        try:
            self.load_config()
            self.initialize()
            
            print("\n=== Plugin Running ===")
            print("Press Ctrl+C to stop\n")
            
            while self.running:
                time.sleep(1)
                
                if hasattr(self.client, 'ws') and self.client.ws:
                    if not self.client.ws.sock or not self.client.ws.sock.connected:
                        print("WebSocket disconnected, reconnecting...")
                        try:
                            self.client.connect_websocket(self.on_websocket_message)
                        except Exception as e:
                            print(f"Reconnect error: {e}")
        
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """停止插件"""
        self.running = False
        
        if self.watcher:
            self.watcher.stop()
        
        if self.client:
            self.client.disconnect_websocket()
        
        print("Plugin stopped")


def main():
    plugin = SoulSyncPlugin()
    plugin.run()


if __name__ == '__main__':
    main()
