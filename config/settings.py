import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置类"""
    
    # 应用配置
    APP_NAME: str = "Multi-Agent Commercial Real Estate Investment Analysis System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PORT: int = 8000
    
    # Redis配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_EXPIRE_TIME: int = int(os.getenv("REDIS_EXPIRE_TIME", "86400"))  # 24小时
    
    # Milvus配置
    MILVUS_HOST: str = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT: int = int(os.getenv("MILVUS_PORT", "19530"))
    MILVUS_COLLECTION_NAME: str = os.getenv("MILVUS_COLLECTION_NAME", "real_estate_knowledge")
    MILVUS_DIMENSION: int = int(os.getenv("MILVUS_DIMENSION", "768"))
    
    # LLM配置
    LLM_MODEL_PATH: str = os.getenv("LLM_MODEL_PATH", "./models/Qwen-7B-Chat")
    LLM_LORA_PATH: str = os.getenv("LLM_LORA_PATH", "./models/qwen7b_lora_realestate")
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/app.log")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
