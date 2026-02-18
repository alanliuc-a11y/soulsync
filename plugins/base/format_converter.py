class FormatConverter:
    """格式转换基类 - 预留接口，方便以后支持不同机器人的文件格式"""
    
    @staticmethod
    def to_cloud(local_content: str, source_type: str) -> str:
        """本地格式转换为云端格式
        
        Args:
            local_content: 本地文件内容
            source_type: 来源类型，如 'openclaw', 'copaw' 等
            
        Returns:
            转换后的云端格式内容
        """
        raise NotImplementedError("Subclasses must implement to_cloud()")
    
    @staticmethod
    def from_cloud(cloud_content: str, target_type: str) -> str:
        """云端格式转换为本地格式
        
        Args:
            cloud_content: 云端内容
            target_type: 目标类型，如 'openclaw', 'copaw' 等
            
        Returns:
            转换后的本地格式内容
        """
        raise NotImplementedError("Subclasses must implement from_cloud()")
