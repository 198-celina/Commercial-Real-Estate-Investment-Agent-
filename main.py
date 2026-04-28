from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints.chat import router as chat_router
from api.v1.endpoints.investment import router as investment_router
from api.v1.endpoints.health import router as health_router
from utils.exception_handler import setup_exception_handlers
from utils.logger import logger

# 创建FastAPI应用
app = FastAPI(
    title="Multi-Agent Commercial Real Estate Investment Analysis System",
    description="基于LangChain的商业地产投资分析系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router, prefix="/api/v1")
app.include_router(investment_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")

# 设置异常处理器
setup_exception_handlers(app)


@app.on_event("startup")
async def startup_event():
    """启动事件"""
    logger.info("Starting Multi-Agent Investment Analysis System...")


@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    logger.info("Shutting down Multi-Agent Investment Analysis System...")


if __name__ == "__main__":
    import uvicorn
    from config.settings import settings
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=True
    )
