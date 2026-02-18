import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class OpenClawWatcher(FileSystemEventHandler):
    """OpenClaw 文件监听器"""
    
    def __init__(self, file_path: str, callback):
        self.file_path = os.path.abspath(file_path)
        self.callback = callback
        self.observer = None
        self.last_modified = 0
        self.debounce_seconds = 1
    
    def start(self):
        """开始监听"""
        directory = os.path.dirname(self.file_path)
        
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                pass
        
        self.observer = Observer()
        self.observer.schedule(self, directory, recursive=False)
        self.observer.start()
        print(f"Started watching: {self.file_path}")
    
    def stop(self):
        """停止监听"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("Stopped watching")
    
    def on_modified(self, event):
        """文件被修改"""
        if event.is_directory:
            return
        
        event_path = os.path.abspath(event.src_path)
        
        if event_path == self.file_path:
            current_time = time.time()
            
            if current_time - self.last_modified > self.debounce_seconds:
                self.last_modified = current_time
                print(f"File modified: {self.file_path}")
                self._trigger_callback('modified', event_path)
    
    def on_created(self, event):
        """文件被创建"""
        if event.is_directory:
            return
        
        event_path = os.path.abspath(event.src_path)
        
        if event_path == self.file_path:
            print(f"File created: {self.file_path}")
            self._trigger_callback('created', event_path)
    
    def _trigger_callback(self, event_type: str, file_path: str = None):
        """触发回调函数"""
        if self.callback:
            self.callback(event_type, file_path)
