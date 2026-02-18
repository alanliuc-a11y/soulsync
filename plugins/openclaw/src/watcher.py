import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class OpenClawMultiWatcher(FileSystemEventHandler):
    """OpenClaw 多文件/目录监听器"""
    
    def __init__(self, workspace: str, watch_paths: list, callback):
        self.workspace = os.path.abspath(workspace)
        self.watch_paths = watch_paths
        self.callback = callback
        self.observer = None
        self.last_events = {}
        self.debounce_seconds = 1
        self.ignore_patterns = ['.tmp', '.swp', '.bak', '~']
    
    def start(self):
        """开始监听"""
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace, exist_ok=True)
        
        self.observer = Observer()
        
        for watch_path in self.watch_paths:
            full_path = os.path.join(self.workspace, watch_path)
            
            if watch_path.endswith('/'):
                dir_name = watch_path.rstrip('/')
                if not os.path.exists(full_path):
                    os.makedirs(full_path, exist_ok=True)
                    print(f"Created directory: {full_path}")
                
                self.observer.schedule(self, full_path, recursive=True)
                print(f"Watching directory: {watch_path}")
            else:
                directory = os.path.dirname(full_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                
                if not os.path.exists(full_path):
                    with open(full_path, 'w', encoding='utf-8') as f:
                        pass
                    print(f"Created file: {watch_path}")
                
                self.observer.schedule(self, os.path.dirname(full_path), recursive=False)
                print(f"Watching file: {watch_path}")
        
        self.observer.start()
        print(f"Started watching {len(self.watch_paths)} paths in {self.workspace}")
    
    def stop(self):
        """停止监听"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("Stopped watching")
    
    def _should_ignore(self, path: str) -> bool:
        """检查是否应该忽略"""
        basename = os.path.basename(path)
        for pattern in self.ignore_patterns:
            if pattern in basename:
                return True
        return False
    
    def _get_relative_path(self, absolute_path: str) -> str:
        """获取相对路径"""
        if absolute_path.startswith(self.workspace):
            relative = absolute_path[len(self.workspace):].lstrip('/')
            return relative
        return absolute_path
    
    def _debounce_check(self, file_path: str) -> bool:
        """防抖检查"""
        current_time = time.time()
        last_time = self.last_events.get(file_path, 0)
        
        if current_time - last_time < self.debounce_seconds:
            return False
        
        self.last_events[file_path] = current_time
        return True
    
    def on_modified(self, event):
        """文件被修改"""
        if event.is_directory:
            return
        
        event_path = os.path.abspath(event.src_path)
        
        if self._should_ignore(event_path):
            return
        
        if self._debounce_check(event_path):
            relative_path = self._get_relative_path(event_path)
            print(f"[Watcher] File modified: {relative_path}")
            self._trigger_callback('modified', relative_path, event_path)
    
    def on_created(self, event):
        """文件被创建"""
        if event.is_directory:
            return
        
        event_path = os.path.abspath(event.src_path)
        
        if self._should_ignore(event_path):
            return
        
        if self._debounce_check(event_path):
            relative_path = self._get_relative_path(event_path)
            print(f"[Watcher] File created: {relative_path}")
            self._trigger_callback('created', relative_path, event_path)
    
    def on_deleted(self, event):
        """文件被删除"""
        if event.is_directory:
            return
        
        event_path = os.path.abspath(event.src_path)
        
        if self._should_ignore(event_path):
            return
        
        relative_path = self._get_relative_path(event_path)
        print(f"[Watcher] File deleted: {relative_path}")
        self._trigger_callback('deleted', relative_path, event_path)
    
    def _trigger_callback(self, event_type: str, relative_path: str, absolute_path: str = None):
        """触发回调函数"""
        if self.callback:
            self.callback(event_type, relative_path, absolute_path)
