from pydantic import BaseModel
from typing import Optional, List, Dict


class ChatResponse(BaseModel):
    """对话响应模型"""
    session_id: str
    message: str
    success: bool
    analysis_type: Optional[str] = None
    metadata: Optional[Dict] = None


class InvestmentAnalysisResponse(BaseModel):
    """投资分析响应模型"""
    session_id: str
    success: bool
    market_analysis: Optional[Dict] = None
    revenue_calculation: Optional[Dict] = None
    risk_compliance: Optional[Dict] = None
    summary: str


class SessionResponse(BaseModel):
    """会话响应模型"""
    session_id: str
    created_at: str
    updated_at: Optional[str] = None
    message_count: int = 0


class KnowledgeResponse(BaseModel):
    """知识库查询响应模型"""
    query: str
    total_results: int
    results: List[Dict]


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    service: str
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    message: str
    code: int
