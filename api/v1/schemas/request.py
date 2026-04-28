from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """对话请求模型"""
    session_id: Optional[str] = Field(description="会话ID，为空时创建新会话")
    message: str = Field(description="用户消息内容")


class InvestmentAnalysisRequest(BaseModel):
    """投资分析请求模型"""
    session_id: Optional[str] = Field(description="会话ID")
    city: str = Field(description="目标城市")
    project_name: Optional[str] = Field(description="项目名称")
    area: Optional[float] = Field(description="建筑面积（平方米）")
    investment_amount: Optional[float] = Field(description="投资金额（万元）")
    property_type: str = Field(default="写字楼", description="物业类型")
    analysis_type: str = Field(default="comprehensive", 
                               description="分析类型：market/revenue/risk/comprehensive")


class SessionCreateRequest(BaseModel):
    """创建会话请求模型"""
    user_id: Optional[str] = Field(description="用户ID")
    metadata: Optional[dict] = Field(description="会话元数据")


class KnowledgeQueryRequest(BaseModel):
    """知识库查询请求模型"""
    query: str = Field(description="查询内容")
    top_k: int = Field(default=10, ge=1, le=20, description="返回数量")
