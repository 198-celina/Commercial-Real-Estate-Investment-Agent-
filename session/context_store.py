import json
from typing import Dict, List, Optional
from datetime import datetime
from session.redis_client import redis_client
from config.settings import settings


class ContextStore:
    """对话上下文存储类"""
    
    def __init__(self):
        self.expire_time = settings.REDIS_EXPIRE_TIME
    
    def _get_session_key(self, session_id: str) -> str:
        """生成会话键名"""
        return f"session:{session_id}"
    
    def save_context(self, session_id: str, context: Dict) -> None:
        """保存对话上下文"""
        key = self._get_session_key(session_id)
        context["updated_at"] = datetime.now().isoformat()
        redis_client.set(key, json.dumps(context), expire_time=self.expire_time)
    
    def get_context(self, session_id: str) -> Optional[Dict]:
        """获取对话上下文"""
        key = self._get_session_key(session_id)
        data = redis_client.get(key)
        if data:
            return json.loads(data.decode('utf-8'))
        return None
    
    def append_message(self, session_id: str, role: str, content: str) -> None:
        """追加消息到对话历史"""
        context = self.get_context(session_id)
        if not context:
            context = {
                "session_id": session_id,
                "history": [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        
        context["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        self.save_context(session_id, context)
    
    def get_history(self, session_id: str) -> List[Dict]:
        """获取对话历史"""
        context = self.get_context(session_id)
        if context and "history" in context:
            return context["history"]
        return []
    
    def clear_context(self, session_id: str) -> None:
        """清除对话上下文"""
        key = self._get_session_key(session_id)
        redis_client.delete(key)
    
    def exists(self, session_id: str) -> bool:
        """检查会话是否存在"""
        key = self._get_session_key(session_id)
        return redis_client.exists(key)
    
    def update_context(self, session_id: str, updates: Dict) -> None:
        """更新对话上下文"""
        context = self.get_context(session_id)
        if context:
            context.update(updates)
            context["updated_at"] = datetime.now().isoformat()
            self.save_context(session_id, context)


context_store = ContextStore()
