import requests


class ProfilesClient:
    """Profiles API 客户端"""
    
    def __init__(self, cloud_url: str, token: str = None):
        self.cloud_url = cloud_url.rstrip('/')
        self.token = token
    
    def _get_headers(self) -> dict:
        """获取请求头"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def set_token(self, token: str):
        """设置 token"""
        self.token = token
    
    def get_profiles(self, path: str = None) -> dict:
        """获取 profiles
        
        Args:
            path: 可选的文件路径
            
        Returns:
            包含 files 列表的字典
        """
        url = f"{self.cloud_url}/api/profiles"
        if path:
            url += f"?path={path}"
        
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {'files': []}
        else:
            error = response.json().get('error', 'Unknown error')
            raise Exception(f"Get profiles failed: {error}")
    
    def upload_profile(self, file_path: str, content: str, version: int) -> dict:
        """上传 profile
        
        Args:
            file_path: 文件路径
            content: 文件内容
            version: 当前版本号
            
        Returns:
            成功时返回 {file_path, version, updated_at}
            冲突时抛出异常
        """
        url = f"{self.cloud_url}/api/profiles"
        data = {
            'file_path': file_path,
            'content': content,
            'version': version
        }
        
        response = requests.post(url, json=data, headers=self._get_headers())
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 409:
            result = response.json()
            raise ConflictError(
                result.get('latest_content', ''),
                result.get('latest_version', 0)
            )
        elif response.status_code == 403:
            error = response.json().get('error', 'Subscription required')
            raise Exception(f"Upload failed: {error}")
        else:
            error = response.json().get('error', 'Unknown error')
            raise Exception(f"Upload failed: {error}")
    
    def sync_profiles(self, since: str = '0') -> dict:
        """增量同步 profiles
        
        Args:
            since: 时间戳
            
        Returns:
            包含 files 列表和 server_time 的字典
        """
        url = f"{self.cloud_url}/api/profiles/sync?since={since}"
        
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            error = response.json().get('error', 'Subscription required')
            raise Exception(f"Sync failed: {error}")
        else:
            error = response.json().get('error', 'Unknown error')
            raise Exception(f"Sync failed: {error}")


class ConflictError(Exception):
    """版本冲突异常"""
    
    def __init__(self, latest_content: str, latest_version: int):
        self.latest_content = latest_content
        self.latest_version = latest_version
        super().__init__(f"Version conflict: latest version is {latest_version}")
