import redis
from typing import Optional, Any
from config.redis_config import redis_config


class RedisClient:
    """Redis客户端封装类"""
    
    def __init__(self):
        self.pool = redis_config.create_connection_pool()
        self.client = redis.Redis(connection_pool=self.pool)
    
    def get(self, key: str) -> Optional[bytes]:
        """获取键值"""
        try:
            return self.client.get(key)
        except Exception as e:
            raise RuntimeError(f"Redis get error: {e}")
    
    def set(self, key: str, value: Any, expire_time: Optional[int] = None) -> bool:
        """设置键值"""
        try:
            if expire_time:
                return self.client.set(key, value, ex=expire_time)
            return self.client.set(key, value)
        except Exception as e:
            raise RuntimeError(f"Redis set error: {e}")
    
    def delete(self, key: str) -> int:
        """删除键"""
        try:
            return self.client.delete(key)
        except Exception as e:
            raise RuntimeError(f"Redis delete error: {e}")
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            raise RuntimeError(f"Redis exists error: {e}")
    
    def hget(self, key: str, field: str) -> Optional[bytes]:
        """获取哈希字段值"""
        try:
            return self.client.hget(key, field)
        except Exception as e:
            raise RuntimeError(f"Redis hget error: {e}")
    
    def hset(self, key: str, field: str, value: Any) -> int:
        """设置哈希字段值"""
        try:
            return self.client.hset(key, field, value)
        except Exception as e:
            raise RuntimeError(f"Redis hset error: {e}")
    
    def hgetall(self, key: str) -> dict:
        """获取哈希所有字段"""
        try:
            return self.client.hgetall(key)
        except Exception as e:
            raise RuntimeError(f"Redis hgetall error: {e}")
    
    def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        try:
            return self.client.expire(key, seconds)
        except Exception as e:
            raise RuntimeError(f"Redis expire error: {e}")
    
    def flushall(self) -> None:
        """清空所有数据"""
        try:
            self.client.flushall()
        except Exception as e:
            raise RuntimeError(f"Redis flushall error: {e}")


redis_client = RedisClient()
