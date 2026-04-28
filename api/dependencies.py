from typing import Optional
from fastapi import Depends, HTTPException
from session.session_manager import session_manager


async def get_session(session_id: Optional[str] = None):
    """获取或创建会话"""
    if session_id and session_manager.exists(session_id):
        return session_id
    
    # 创建新会话
    return session_manager.create_session()


async def require_session(session_id: str):
    """要求会话必须存在"""
    if not session_manager.exists(session_id):
        raise HTTPException(status_code=404, detail="会话不存在")
    return session_id
