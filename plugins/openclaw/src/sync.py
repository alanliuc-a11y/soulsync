import os
import time
from src.profiles import ProfilesClient, ConflictError


class ProfileSync:
    """多文件同步逻辑"""
    
    def __init__(self, client: ProfilesClient, version_manager, workspace: str):
        self.client = client
        self.version_manager = version_manager
        self.workspace = os.path.abspath(workspace)
        self.is_syncing = False
    
    def pull_all(self) -> int:
        """从云端拉取所有文件
        
        Returns:
            拉取的文件数量
        """
        print("[Sync] Pulling all profiles from cloud...")
        self.is_syncing = True
        
        try:
            result = self.client.sync_profiles(since='0')
            files = result.get('files', [])
            
            if not files:
                print("[Sync] No files in cloud")
                return 0
            
            count = 0
            for file_info in files:
                file_path = file_info.get('file_path')
                content = file_info.get('content')
                version = file_info.get('version')
                
                if file_path and content is not None:
                    self._write_local_file(file_path, content)
                    self.version_manager.set_version(file_path, version)
                    count += 1
                    print(f"[Sync] Downloaded: {file_path} (v{version})")
            
            print(f"[Sync] Pulled {count} files")
            return count
        finally:
            self.is_syncing = False
    
    def push_file(self, file_path: str):
        """推送单个文件到云端
        
        Args:
            file_path: 文件相对路径
        """
        if self.is_syncing:
            print(f"[Sync] Skipping push, currently syncing: {file_path}")
            return
        
        print(f"[Sync] Pushing file: {file_path}")
        
        content = self._read_local_file(file_path)
        if content is None:
            print(f"[Sync] File not found or read error: {file_path}")
            return
        
        local_version = self.version_manager.get_version(file_path)
        
        try:
            result = self.client.upload_profile(file_path, content, local_version)
            
            new_version = result.get('version')
            self.version_manager.set_version(file_path, new_version)
            
            print(f"[Sync] Uploaded: {file_path} (v{new_version})")
            
        except ConflictError as e:
            print(f"[Sync] Version conflict for {file_path}, pulling latest...")
            
            self._write_local_file(file_path, e.latest_content)
            self.version_manager.set_version(file_path, e.latest_version)
            
            print(f"[Sync] Resolved conflict: {file_path} (now v{e.latest_version})")
        
        except Exception as e:
            print(f"[Sync] Upload error: {e}")
    
    def on_remote_change(self, file_path: str, version: int):
        """远程文件变化回调
        
        Args:
            file_path: 文件相对路径
            version: 新版本号
        """
        print(f"[Sync] Remote change detected: {file_path} (v{version})")
        
        local_version = self.version_manager.get_version(file_path)
        
        if version > local_version:
            try:
                result = self.client.get_profiles(path=file_path)
                files = result.get('files', [])
                
                if files:
                    file_info = files[0]
                    content = file_info.get('content')
                    
                    self._write_local_file(file_path, content)
                    self.version_manager.set_version(file_path, version)
                    
                    print(f"[Sync] Pulled remote change: {file_path} (v{version})")
            except Exception as e:
                print(f"[Sync] Pull remote change error: {e}")
    
    def _read_local_file(self, file_path: str) -> str:
        """读取本地文件"""
        full_path = os.path.join(self.workspace, file_path)
        
        if not os.path.exists(full_path):
            return None
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[Sync] Read error {file_path}: {e}")
            return None
    
    def _write_local_file(self, file_path: str, content: str):
        """写入本地文件"""
        full_path = os.path.join(self.workspace, file_path)
        
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"[Sync] Write error {file_path}: {e}")
