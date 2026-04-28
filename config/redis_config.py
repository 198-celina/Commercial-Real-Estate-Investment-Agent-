import redis
from typing import Optional
from config.settings import settings


class RedisConfig:
    """Redis配置类"""
    
    HOST = settings.REDIS_HOST
    PORT = settings.REDIS_PORT
    DB = settings.REDIS_DB
    PASSWORD = settings.REDIS_PASSWORD
    EXPIRE_TIME = settings.REDIS_EXPIRE_TIME
    
    # 连接池配置
    MAX_CONNECTIONS = 100
    MIN_IDLE_CONNECTIONS = 10
    CONNECT_TIMEOUT = 5
    SOCKET_TIMEOUT = 5
    
    @classmethod
    def create_connection_pool(cls) -> redis.ConnectionPool:
        """创建Redis连接池"""
        return redis.ConnectionPool(
            host=cls.HOST,
            port=cls.PORT,
            db=cls.DB,
            password=cls.PASSWORD,
            max_connections=cls.MAX_CONNECTIONS,
            socket_connect_timeout=cls.CONNECT_TIMEOUT,
            socket_timeout=cls.SOCKET_TIMEOUT
        )
    
    @classmethod
    def get_client(cls, pool: Optional[redis.ConnectionPool] = None) -> redis.Redis:
        """获取Redis客户端"""
        if pool:
            return redis.Redis(connection_pool=pool)
        return redis.Redis(
            host=cls.HOST,
            port=cls.PORT,
            db=cls.DB,
            password=cls.PASSWORD
        )


redis_config = RedisConfig()
