class BaseWatcher:
    """文件监听基类"""
    
    def __init__(self, path: str, callback):
        self.path = path
        self.callback = callback
        self.watcher = None
    
    def start(self):
        """开始监听"""
        raise NotImplementedError("Subclasses must implement start()")
    
    def stop(self):
        """停止监听"""
        raise NotImplementedError("Subclasses must implement stop()")
    
    def _trigger_callback(self, event_type: str, file_path: str = None):
        """触发回调函数
        
        Args:
            event_type: 事件类型，如 'modified', 'created', 'deleted'
            file_path: 触发事件的文件路径
        """
        if self.callback:
            self.callback(event_type, file_path)
