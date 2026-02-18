import json
import os
import requests
from urllib.parse import urljoin


class BaseClient:
    """API/WS 客户端基类"""
    
    def __init__(self, config: dict):
        self.config = config
        self.cloud_url = config.get('cloud_url', '').rstrip('/')
        self.token = None
        self.user_id = None
        self.device_id = self._load_device_id()
    
    def _load_device_id(self) -> str:
        """加载或生成设备ID"""
        device_id_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'device_id')
        
        if os.path.exists(device_id_file):
            with open(device_id_file, 'r') as f:
                return f.read().strip()
        
        return None
    
    def _save_device_id(self, device_id: str):
        """保存设备ID"""
        device_id_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'device_id')
        with open(device_id_file, 'w') as f:
            f.write(device_id)
        self.device_id = device_id
    
    def _save_token(self, token: str):
        """保存 token"""
        token_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token')
        with open(token_file, 'w') as f:
            f.write(token)
        self.token = token
    
    def _load_token(self) -> str:
        """加载 token"""
        token_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token')
        
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                return f.read().strip()
        
        return None
    
    def _get_headers(self) -> dict:
        """获取请求头"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def register_or_login(self, device_id: str = None, email: str = None, password: str = None) -> dict:
        """自动注册或登录
        
        Args:
            device_id: 设备ID，若为None则使用保存的设备ID
            email: 邮箱 (首次注册需要)
            password: 密码 (首次注册需要)
            
        Returns:
            包含 user_id, token 等信息的字典
        """
        raise NotImplementedError("Subclasses must implement register_or_login()")
    
    def upload_memory(self, content: str) -> dict:
        """上传记忆
        
        Args:
            content: 记忆内容
            
        Returns:
            上传结果
        """
        raise NotImplementedError("Subclasses must implement upload_memory()")
    
    def download_memory(self) -> dict:
        """下载记忆
        
        Returns:
            包含 content, version 等信息的字典
        """
        raise NotImplementedError("Subclasses must implement download_memory()")
    
    def get_profile(self) -> dict:
        """获取用户信息
        
        Returns:
            用户信息
        """
        raise NotImplementedError("Subclasses must implement get_profile()")
    
    def connect_websocket(self, on_message_callback):
        """连接 WebSocket
        
        Args:
            on_message_callback: 消息回调函数
        """
        raise NotImplementedError("Subclasses must implement connect_websocket()")
