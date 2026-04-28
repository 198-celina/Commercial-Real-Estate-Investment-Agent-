import uuid
from typing import Optional, Dict
from session.context_store import context_store
from datetime import datetime


class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        self.context_store = context_store
    
    def create_session(self) -> str:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        context = {
            "session_id": session_id,
            "history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "metadata": {}
        }
        self.context_store.save_context(session_id, context)
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """获取会话信息"""
        if self.context_store.exists(session_id):
            return self.context_store.get_context(session_id)
        return None
    
    def update_session(self, session_id: str, updates: Dict) -> None:
        """更新会话信息"""
        self.context_store.update_context(session_id, updates)
    
    def delete_session(self, session_id: str) -> None:
        """删除会话"""
        self.context_store.clear_context(session_id)
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """添加消息到会话"""
        self.context_store.append_message(session_id, role, content)
    
    def get_messages(self, session_id: str) -> list:
        """获取会话消息列表"""
        return self.context_store.get_history(session_id)
    
    def exists(self, session_id: str) -> bool:
        """检查会话是否存在"""
        return self.context_store.exists(session_id)


session_manager = SessionManager()
