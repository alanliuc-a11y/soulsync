import os


class OpenClawSync:
    """OpenClaw 同步逻辑"""
    
    def __init__(self, client, watcher):
        self.client = client
        self.watcher = watcher
        self.memory_file = None
        self.local_version = 0
        self.is_uploading = False
    
    def set_memory_file(self, file_path: str):
        """设置记忆文件路径"""
        self.memory_file = os.path.abspath(file_path)
    
    def pull(self) -> str:
        """从云端拉取记忆
        
        Returns:
            拉取的记忆内容
        """
        print("Pulling memory from cloud...")
        
        result = self.client.download_memory()
        
        content = result.get('content', '')
        self.local_version = result.get('version', 0)
        
        if content:
            self._write_memory_file(content)
            print(f"Pulled memory, version: {self.local_version}")
        else:
            print("No memory in cloud, local file unchanged")
        
        return content
    
    def push(self, content: str = None):
        """推送记忆到云端
        
        Args:
            content: 要推送的记忆内容，若为None则从本地文件读取
        """
        if self.is_uploading:
            print("Already uploading, skipping...")
            return
        
        self.is_uploading = True
        
        try:
            if content is None:
                content = self._read_memory_file()
            
            if not content:
                print("Nothing to upload (empty content)")
                return
            
            print(f"Pushing memory to cloud ({len(content)} bytes)...")
            
            result = self.client.upload_memory(content)
            
            self.local_version = result.get('version', self.local_version + 1)
            
            print(f"Pushed memory, new version: {self.local_version}")
        finally:
            self.is_uploading = False
    
    def sync(self, local_content: str = None) -> str:
        """同步记忆
        
        Args:
            local_content: 本地记忆内容
            
        Returns:
            同步后的记忆内容
        """
        if self.is_uploading:
            return local_content
        
        remote = self.pull()
        
        if remote and remote != local_content:
            print("Remote has newer content")
            return remote
        
        if local_content:
            self.push(local_content)
        
        return local_content
    
    def on_remote_change(self, version: int):
        """远程发生变化时的回调"""
        print(f"Remote changed, new version: {version}")
        
        if version > self.local_version:
            self.pull()
    
    def _read_memory_file(self) -> str:
        """读取本地记忆文件"""
        if not self.memory_file or not os.path.exists(self.memory_file):
            return ''
        
        with open(self.memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _write_memory_file(self, content: str):
        """写入本地记忆文件"""
        if not self.memory_file:
            raise ValueError("Memory file not set")
        
        directory = os.path.dirname(self.memory_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            f.write(content)
