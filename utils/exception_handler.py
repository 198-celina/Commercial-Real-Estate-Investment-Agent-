from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.logger import logger


def setup_exception_handlers(app: FastAPI):
    """设置全局异常处理器"""
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """全局异常处理"""
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": str(exc),
                "code": 500
            }
        )
    
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception):
        """404错误处理"""
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "message": "The requested resource was not found",
                "code": 404
            }
        )
    
    @app.exception_handler(400)
    async def bad_request_handler(request: Request, exc: Exception):
        """400错误处理"""
        return JSONResponse(
            status_code=400,
            content={
                "error": "Bad Request",
                "message": str(exc),
                "code": 400
            }
        )
