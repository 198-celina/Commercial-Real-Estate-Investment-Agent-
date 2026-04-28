from fastapi import APIRouter
from api.v1.schemas.response import HealthResponse
from datetime import datetime

router = APIRouter(prefix="/health", tags=["健康检查"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        service="Multi-Agent Commercial Real Estate Investment Analysis System",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@router.get("/ready")
async def readiness_check():
    """就绪检查"""
    return {"status": "ready", "timestamp": datetime.now().isoformat()}
