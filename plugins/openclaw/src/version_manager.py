import json
import os


class VersionManager:
    """本地版本管理"""
    
    def __init__(self, versions_file: str):
        self.versions_file = versions_file
        self.versions = {}
        self.load()
    
    def load(self):
        """加载版本文件"""
        if os.path.exists(self.versions_file):
            try:
                with open(self.versions_file, 'r', encoding='utf-8') as f:
                    self.versions = json.load(f)
            except Exception as e:
                print(f"Failed to load versions file: {e}")
                self.versions = {}
        else:
            self.versions = {}
    
    def save(self):
        """保存版本文件"""
        try:
            directory = os.path.dirname(self.versions_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(self.versions_file, 'w', encoding='utf-8') as f:
                json.dump(self.versions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save versions file: {e}")
    
    def get_version(self, file_path: str) -> int:
        """获取文件版本"""
        return self.versions.get(file_path, 0)
    
    def set_version(self, file_path: str, version: int):
        """设置文件版本"""
        self.versions[file_path] = version
        self.save()
    
    def increment_version(self, file_path: str) -> int:
        """递增版本"""
        current = self.get_version(file_path)
        new_version = current + 1
        self.set_version(file_path, new_version)
        return new_version
    
    def update_versions(self, updates: dict):
        """批量更新版本"""
        for file_path, version in updates.items():
            self.versions[file_path] = version
        self.save()
    
    def get_all_versions(self) -> dict:
        """获取所有版本"""
        return self.versions.copy()
