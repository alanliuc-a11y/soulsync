import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'base'))

from src.client import OpenClawClient
from src.watcher import OpenClawMultiWatcher
from src.version_manager import VersionManager
from src.profiles import ProfilesClient
from src.sync import ProfileSync


class SoulSyncPlugin:
    """SoulSync OpenClaw 插件主类"""
    
    def __init__(self):
        self.config = None
        self.client = None
        self.profiles_client = None
        self.watcher = None
        self.version_manager = None
        self.profile_sync = None
        self.running = False
    
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        workspace = self.config.get('workspace', './workspace')
        workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', workspace))
        
        watch_files = self.config.get('watch_files', ['MEMORY.md', 'memory/'])
        
        self.config['workspace'] = workspace
        self.config['watch_files'] = watch_files
        
        print(f"Config loaded:")
        print(f"  Cloud URL: {self.config.get('cloud_url')}")
        print(f"  Workspace: {workspace}")
        print(f"  Watch files: {watch_files}")
    
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
        
        versions_file = os.path.join(os.path.dirname(__file__), '..', 'versions.json')
        self.version_manager = VersionManager(versions_file)
        
        self.profiles_client = ProfilesClient(
            self.config.get('cloud_url'),
            self.client.token
        )
        
        self.profile_sync = ProfileSync(
            self.profiles_client,
            self.version_manager,
            self.config.get('workspace')
        )
        
        print("Pulling all profiles from cloud...")
        self.profile_sync.pull_all()
        
        print("\nStarting file watcher...")
        watch_files = self.config.get('watch_files', [])
        self.watcher = OpenClawMultiWatcher(
            self.config.get('workspace'),
            watch_files,
            self.on_file_change
        )
        self.watcher.start()
        
        print("\nConnecting to WebSocket...")
        self.client.connect_websocket(self.on_websocket_message)
        
        self.running = True
    
    def on_file_change(self, event_type: str, relative_path: str, absolute_path: str = None):
        """文件变化回调"""
        print(f"\n[File {event_type}] {relative_path}")
        
        if event_type in ['modified', 'created']:
            time.sleep(0.5)
            
            try:
                self.profile_sync.push_file(relative_path)
                print(f"Upload completed: {relative_path}")
            except Exception as e:
                print(f"Upload error: {e}")
        
        elif event_type == 'deleted':
            print(f"File deleted (not synced to cloud): {relative_path}")
    
    def on_websocket_message(self, data: dict):
        """WebSocket 消息回调"""
        event = data.get('event')
        
        if event == 'file_updated':
            file_path = data.get('file_path')
            version = data.get('version')
            print(f"\n[WebSocket] File updated: {file_path} (v{version})")
            try:
                self.profile_sync.on_remote_change(file_path, version)
            except Exception as e:
                print(f"Sync error: {e}")
        
        elif event == 'new_memory':
            print(f"\n[WebSocket] New memory available!")
            try:
                self.profile_sync.pull_all()
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
        print("SoulSync OpenClaw Plugin (Multi-File Sync)")
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
