from fastapi import APIRouter, HTTPException
from api.v1.schemas.request import ChatRequest
from api.v1.schemas.response import ChatResponse
from agent.main_agent import MainAgent
from session.session_manager import session_manager

router = APIRouter(prefix="/chat", tags=["对话"])
main_agent = MainAgent()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """对话接口"""
    try:
        # 检查会话是否存在，不存在则创建
        if not request.session_id or not session_manager.exists(request.session_id):
            session_id = session_manager.create_session()
        else:
            session_id = request.session_id
        
        # 添加用户消息到会话
        session_manager.add_message(session_id, "user", request.message)
        
        # 调用主Agent处理
        result = main_agent.run(request.message)
        
        # 添加Agent响应到会话
        response_text = str(result.get("summary", "") or result.get("analysis_results", "分析完成"))
        session_manager.add_message(session_id, "assistant", response_text)
        
        return ChatResponse(
            session_id=session_id,
            message=response_text,
            success=result.get("success", False),
            analysis_type=result.get("intents", ["unknown"])[0] if result.get("intents") else None,
            metadata={"intents": result.get("intents")}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """获取对话历史"""
    try:
        if not session_manager.exists(session_id):
            raise HTTPException(status_code=404, detail="会话不存在")
        
        messages = session_manager.get_messages(session_id)
        return {"session_id": session_id, "messages": messages}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    try:
        if not session_manager.exists(session_id):
            raise HTTPException(status_code=404, detail="会话不存在")
        
        session_manager.delete_session(session_id)
        return {"success": True, "message": "会话已删除"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
