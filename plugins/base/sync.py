class BaseSync:
    """同步基类"""
    
    def __init__(self, client, watcher):
        self.client = client
        self.watcher = watcher
    
    def pull(self) -> str:
        """从云端拉取记忆
        
        Returns:
            拉取的记忆内容
        """
        raise NotImplementedError("Subclasses must implement pull()")
    
    def push(self, content: str):
        """推送记忆到云端
        
        Args:
            content: 要推送的记忆内容
        """
        raise NotImplementedError("Subclasses must implement push()")
    
    def sync(self, local_content: str) -> str:
        """同步记忆
        
        Args:
            local_content: 本地记忆内容
            
        Returns:
            同步后的记忆内容
        """
        raise NotImplementedError("Subclasses must implement sync()")
    
    def on_remote_change(self, version: int):
        """远程发生变化时的回调
        
        Args:
            version: 新的版本号
        """
        raise NotImplementedError("Subclasses must implement on_remote_change()")
