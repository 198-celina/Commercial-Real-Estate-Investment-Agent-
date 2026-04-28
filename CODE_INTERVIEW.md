# 商业地产投资分析系统 - 代码面试题

## 概述

本文档整理了商业地产投资分析系统技术面试中可能涉及的代码类问题，涵盖以下技术领域：

1. **FastAPI 接口开发**
2. **Redis 会话管理**
3. **限流熔断实现**
4. **RAG 多路召回与排序**
5. **Agent 工具调用机制**

---

## 一、FastAPI 接口开发

### 问题 1：实现带参数校验和缓存的投资分析接口

**需求：**
实现一个商业地产投资分析查询接口，要求：
- 使用 Pydantic 进行参数校验
- 集成 Redis 响应缓存
- 处理异常并返回友好提示

**参考实现：**

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from redis import Redis
from typing import Optional
import json
import uuid
from datetime import datetime

app = FastAPI(title="商业地产投资分析 API")
redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)


class InvestmentQuery(BaseModel):
    """投资分析查询参数"""
    city: str = Field(..., description="目标城市", min_length=1, max_length=50)
    property_type: str = Field(default="写字楼", description="物业类型", 
                               regex="^(写字楼|商铺|工业厂房|仓储)$")
    area: Optional[float] = Field(None, ge=0, description="建筑面积（平方米）")
    investment_amount: Optional[float] = Field(None, ge=0, description="投资金额（万元）")


def get_cache_key(query: InvestmentQuery) -> str:
    """生成缓存键"""
    return f"investment:analyze:{query.city}:{query.property_type}:{query.area or 0}:{query.investment_amount or 0}"


@app.get("/api/v1/investment/analyze", response_model=dict)
async def analyze_investment(query: InvestmentQuery = Depends()):
    """
    商业地产投资分析接口
    - 支持参数校验
    - 支持 Redis 缓存（5分钟有效期）
    - 异常处理
    """
    # 尝试从缓存获取
    cache_key = get_cache_key(query)
    cached_result = redis.get(cache_key)
    
    if cached_result:
        return json.loads(cached_result)
    
    try:
        # 模拟投资分析逻辑
        result = {
            "query": query.dict(),
            "analysis": {
                "market": {
                    "city": query.city,
                    "property_type": query.property_type,
                    "avg_rent": 150,  # 元/平方米/月
                    "vacancy_rate": 0.12,
                    "price_trend": "stable"
                },
                "revenue": {
                    "roi": 0.085,
                    "payback_period": 11.8,
                    "irr": 0.12
                },
                "risk": {
                    "level": "medium",
                    "factors": ["政策风险", "市场波动"]
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # 缓存结果（5分钟）
        redis.setex(cache_key, 300, json.dumps(result))
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


# 依赖注入示例：获取当前会话
async def get_session(session_id: Optional[str] = None):
    if session_id and redis.exists(f"session:{session_id}"):
        return session_id
    # 创建新会话
    new_session_id = str(uuid.uuid4())
    redis.setex(f"session:{new_session_id}", 86400, json.dumps({
        "created_at": datetime.now().isoformat(),
        "message_count": 0
    }))
    return new_session_id
```

---

## 二、Redis 会话管理

### 问题 2：实现分布式会话管理器

**需求：**
实现一个基于 Redis 的分布式会话管理器，支持：
- 会话创建与销毁
- 会话数据读写
- 会话过期自动清理

**参考实现：**

```python
import json
import uuid
from datetime import datetime, timedelta
from redis import Redis
from typing import Optional, Any


class SessionManager:
    """基于 Redis 的分布式会话管理器"""
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, db: int = 0):
        self.redis = Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)
        self.default_expire = timedelta(hours=24)  # 默认24小时过期
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "message_count": 0
        }
        # 使用 Hash 结构存储会话数据
        self.redis.hset(f"session:{session_id}", mapping=session_data)
        self.redis.expire(f"session:{session_id}", self.default_expire)
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话数据"""
        session_data = self.redis.hgetall(f"session:{session_id}")
        if not session_data:
            return None
        
        # 刷新过期时间
        self.redis.expire(f"session:{session_id}", self.default_expire)
        return session_data
    
    def set_session_data(self, session_id: str, key: str, value: Any):
        """设置会话数据"""
        if not self.exists(session_id):
            raise ValueError(f"Session {session_id} does not exist")
        
        self.redis.hset(f"session:{session_id}", key, json.dumps(value))
        self.redis.expire(f"session:{session_id}", self.default_expire)
    
    def get_session_data(self, session_id: str, key: str) -> Optional[Any]:
        """获取会话数据"""
        data = self.redis.hget(f"session:{session_id}", key)
        if data:
            self.redis.expire(f"session:{session_id}", self.default_expire)
            return json.loads(data)
        return None
    
    def update_message_count(self, session_id: str):
        """增加消息计数"""
        self.redis.hincrby(f"session:{session_id}", "message_count", 1)
        self.redis.hset(f"session:{session_id}", "updated_at", datetime.now().isoformat())
        self.redis.expire(f"session:{session_id}", self.default_expire)
    
    def exists(self, session_id: str) -> bool:
        """检查会话是否存在"""
        return self.redis.exists(f"session:{session_id}") > 0
    
    def delete_session(self, session_id: str):
        """删除会话"""
        self.redis.delete(f"session:{session_id}")


# 使用示例
if __name__ == "__main__":
    session_manager = SessionManager()
    
    # 创建会话
    session_id = session_manager.create_session(user_id="user123")
    print(f"Created session: {session_id}")
    
    # 设置会话数据
    session_manager.set_session_data(session_id, "history", ["你好", "我想咨询投资分析"])
    
    # 获取会话数据
    history = session_manager.get_session_data(session_id, "history")
    print(f"Session history: {history}")
    
    # 更新消息计数
    session_manager.update_message_count(session_id)
    
    # 检查会话
    print(f"Session exists: {session_manager.exists(session_id)}")
    
    # 删除会话
    session_manager.delete_session(session_id)
```

---

## 三、限流熔断实现

### 问题 3：基于 Token Bucket 的限流装饰器

**需求：**
实现一个基于 Token Bucket 算法的限流装饰器，要求：
- 支持自定义令牌桶大小和速率
- 使用 Redis 实现分布式限流
- 返回 429 状态码表示限流

**参考实现：**

```python
from functools import wraps
from redis import Redis
from fastapi import HTTPException
from datetime import timedelta


class RateLimiter:
    """基于 Token Bucket 的分布式限流器"""
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, db: int = 0):
        self.redis = Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)
    
    def _get_tokens(self, key: str, max_tokens: int, rate: int) -> int:
        """获取当前令牌数"""
        # 令牌桶键和时间戳键
        tokens_key = f"rate_limit:tokens:{key}"
        timestamp_key = f"rate_limit:timestamp:{key}"
        
        # 管道操作，保证原子性
        pipe = self.redis.pipeline()
        pipe.get(tokens_key)
        pipe.get(timestamp_key)
        pipe.getset(timestamp_key, str(datetime.now().timestamp()))
        
        tokens_str, old_timestamp_str, _ = pipe.execute()
        
        tokens = int(tokens_str) if tokens_str else max_tokens
        old_timestamp = float(old_timestamp_str) if old_timestamp_str else 0
        
        # 计算应该补充的令牌数
        now = datetime.now().timestamp()
        elapsed = now - old_timestamp
        
        # 根据速率补充令牌
        new_tokens = min(max_tokens, tokens + int(elapsed * rate))
        
        # 更新令牌数
        self.redis.set(tokens_key, new_tokens)
        
        return new_tokens
    
    def rate_limit(self, max_tokens: int = 100, rate: int = 10):
        """
        限流装饰器
        :param max_tokens: 最大令牌数（桶容量）
        :param rate: 每秒生成令牌数
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 使用函数名作为限流键
                key = func.__name__
                
                # 获取当前令牌数
                tokens = self._get_tokens(key, max_tokens, rate)
                
                if tokens <= 0:
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "Too Many Requests",
                            "message": "请求过于频繁，请稍后重试",
                            "retry_after": 60  # 建议重试时间（秒）
                        }
                    )
                
                # 消耗令牌
                self.redis.decr(f"rate_limit:tokens:{key}")
                return func(*args, **kwargs)
            return wrapper
        return decorator


# 使用示例
app = FastAPI()
limiter = RateLimiter()

@app.get("/api/v1/analysis")
@limiter.rate_limit(max_tokens=100, rate=10)
async def get_analysis(city: str):
    return {"city": city, "analysis": "投资分析结果"}


# 简化版本（单进程）
def simple_rate_limit(max_calls: int, time_window: int = 60):
    """
    简单的内存限流装饰器（单进程）
    :param max_calls: 时间窗口内最大调用次数
    :param time_window: 时间窗口（秒）
    """
    call_counts = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now().timestamp()
            key = func.__name__
            
            # 清理过期记录
            if key not in call_counts:
                call_counts[key] = []
            call_counts[key] = [t for t in call_counts[key] if now - t < time_window]
            
            if len(call_counts[key]) >= max_calls:
                raise HTTPException(status_code=429, detail="Too Many Requests")
            
            call_counts[key].append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 四、RAG 多路召回与排序

### 问题 4：实现 RRF（Reciprocal Rank Fusion）融合排序

**需求：**
实现 RRF 算法，将多路召回结果融合排序，要求：
- 支持任意数量的召回源
- 可配置 RRF 参数 k
- 返回排序后的文档列表

**参考实现：**

```python
from collections import defaultdict
from typing import List, Tuple, Any


def rrf_fusion(results: List[List[Any]], k: int = 60) -> List[Tuple[Any, float]]:
    """
    RRF（Reciprocal Rank Fusion）融合排序算法
    :param results: 多路召回结果列表，每路是文档列表
    :param k: RRF 参数，通常取 60
    :return: 融合后的文档排名（文档, 分数），按分数降序排列
    """
    scores = defaultdict(float)
    
    # 遍历每路召回结果
    for result_list in results:
        # 遍历每个文档，记录其排名
        for rank, doc in enumerate(result_list, 1):
            # RRF 公式：score += 1 / (k + rank)
            scores[doc] += 1.0 / (k + rank)
    
    # 按分数降序排序
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs


def weighted_rrf_fusion(results: List[List[Any]], weights: List[float], k: int = 60) -> List[Tuple[Any, float]]:
    """
    带权重的 RRF 融合
    :param results: 多路召回结果列表
    :param weights: 每路的权重
    :param k: RRF 参数
    :return: 融合后的文档排名
    """
    if len(results) != len(weights):
        raise ValueError("结果数量必须与权重数量匹配")
    
    # 归一化权重
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    scores = defaultdict(float)
    
    for idx, result_list in enumerate(results):
        weight = normalized_weights[idx]
        for rank, doc in enumerate(result_list, 1):
            scores[doc] += weight / (k + rank)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# 使用示例
if __name__ == "__main__":
    # 三路召回结果
    ann_results = ["doc1", "doc2", "doc3", "doc4", "doc5"]  # 向量检索
    bm25_results = ["doc2", "doc4", "doc1", "doc6", "doc7"]  # BM25
    semantic_results = ["doc3", "doc1", "doc5", "doc2", "doc8"]  # 语义匹配
    
    # 基础 RRF 融合
    basic_result = rrf_fusion([ann_results, bm25_results, semantic_results])
    print("基础 RRF 融合结果:")
    for doc, score in basic_result[:5]:
        print(f"  {doc}: {score:.4f}")
    
    # 带权重的 RRF 融合（向量检索权重最高）
    weighted_result = weighted_rrf_fusion(
        [ann_results, bm25_results, semantic_results],
        weights=[0.5, 0.3, 0.2]
    )
    print("\n带权重的 RRF 融合结果:")
    for doc, score in weighted_result[:5]:
        print(f"  {doc}: {score:.4f}")
```

---

## 五、Agent 工具调用机制

### 问题 5：实现 Agent 工具调用框架

**需求：**
实现一个简单的 Agent 工具调用框架，支持：
- 工具注册与发现
- 参数校验
- 调用结果处理

**参考实现：**

```python
from typing import Any, Dict, List, Callable, Optional
from pydantic import BaseModel, ValidationError
from functools import wraps


class ToolResult(BaseModel):
    """工具调用结果"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class ToolMetadata(BaseModel):
    """工具元数据"""
    name: str
    description: str
    parameters: Dict[str, type]


class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.metadata: Dict[str, ToolMetadata] = {}
    
    def register_tool(self, name: str, description: str, parameters: Dict[str, type]):
        """
        注册工具装饰器
        :param name: 工具名称
        :param description: 工具描述
        :param parameters: 参数定义（参数名: 类型）
        """
        def decorator(func):
            @wraps(func)
            def wrapper(**kwargs):
                # 参数校验
                for param_name, param_type in parameters.items():
                    if param_name in kwargs:
                        if not isinstance(kwargs[param_name], param_type):
                            return ToolResult(
                                success=False,
                                error=f"参数 {param_name} 类型错误，期望 {param_type.__name__}"
                            )
                
                try:
                    result = func(**kwargs)
                    return ToolResult(success=True, data=result)
                except Exception as e:
                    return ToolResult(success=False, error=str(e))
            
            self.tools[name] = wrapper
            self.metadata[name] = ToolMetadata(
                name=name,
                description=description,
                parameters=parameters
            )
            return wrapper
        return decorator
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """获取工具"""
        return self.tools.get(name)
    
    def get_tool_metadata(self, name: str) -> Optional[ToolMetadata]:
        """获取工具元数据"""
        return self.metadata.get(name)
    
    def list_tools(self) -> List[str]:
        """列出所有工具"""
        return list(self.tools.keys())


# 示例：创建工具注册中心
tool_registry = ToolRegistry()


# 注册市场分析工具
@tool_registry.register_tool(
    name="get_market_data",
    description="获取商业地产市场数据",
    parameters={"city": str, "property_type": str}
)
def get_market_data(city: str, property_type: str = "写字楼") -> Dict[str, Any]:
    """获取市场数据"""
    return {
        "city": city,
        "property_type": property_type,
        "avg_rent": 150,
        "vacancy_rate": 0.12,
        "price_per_sqm": 35000
    }


# 注册收益测算工具
@tool_registry.register_tool(
    name="calculate_revenue",
    description="计算投资收益",
    parameters={"investment": float, "area": float, "avg_rent": float}
)
def calculate_revenue(investment: float, area: float, avg_rent: float) -> Dict[str, Any]:
    """计算投资收益"""
    monthly_income = area * avg_rent / 10000  # 万元
    annual_income = monthly_income * 12
    operating_expenses = annual_income * 0.3  # 运营成本占比30%
    net_income = annual_income - operating_expenses
    roi = net_income / investment
    
    return {
        "monthly_income": round(monthly_income, 2),
        "annual_income": round(annual_income, 2),
        "net_income": round(net_income, 2),
        "roi": round(roi * 100, 2),
        "payback_period": round(investment / net_income, 1)
    }


# 使用示例
if __name__ == "__main__":
    # 列出所有工具
    print("可用工具:", tool_registry.list_tools())
    
    # 调用市场分析工具
    result = tool_registry.get_tool("get_market_data")(city="上海", property_type="写字楼")
    print("\n市场数据:", result.dict())
    
    # 调用收益测算工具
    result = tool_registry.get_tool("calculate_revenue")(
        investment=5000, area=2000, avg_rent=180
    )
    print("收益测算:", result.dict())
    
    # 调用时参数类型错误
    result = tool_registry.get_tool("calculate_revenue")(
        investment="5000", area=2000, avg_rent=180
    )
    print("参数错误:", result.dict())
```

---

## 六、向量数据库操作

### 问题 6：Milvus 向量检索封装

**需求：**
封装 Milvus 向量检索操作，支持：
- 向量插入
- 相似度搜索
- 索引管理

**参考实现：**

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from typing import List, Tuple, Any
import numpy as np


class MilvusVectorStore:
    """Milvus 向量存储封装"""
    
    def __init__(self, host: str = "localhost", port: int = 19530):
        self.host = host
        self.port = port
        self.collection = None
    
    def connect(self):
        """连接 Milvus"""
        connections.connect("default", host=self.host, port=self.port)
    
    def disconnect(self):
        """断开连接"""
        connections.disconnect("default")
    
    def create_collection(self, collection_name: str, dimension: int = 768):
        """创建向量集合"""
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
        
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=100)
        ]
        
        schema = CollectionSchema(fields, description="商业地产知识库")
        self.collection = Collection(collection_name, schema)
        
        # 创建 HNSW 索引
        index_params = {
            "metric_type": "L2",
            "index_type": "HNSW",
            "params": {"M": 16, "efConstruction": 200}
        }
        self.collection.create_index("embedding", index_params)
        self.collection.load()
    
    def insert(self, embeddings: List[np.ndarray], texts: List[str], sources: List[str]):
        """插入向量数据"""
        if len(embeddings) != len(texts) or len(texts) != len(sources):
            raise ValueError("嵌入向量、文本和来源数量必须一致")
        
        entities = [
            [e.tolist() for e in embeddings],
            texts,
            sources
        ]
        
        insert_result = self.collection.insert(entities)
        self.collection.flush()
        return insert_result.primary_keys
    
    def search(self, query_embedding: np.ndarray, top_k: int = 10, 
               filter: str = None) -> List[Tuple[str, float]]:
        """
        向量搜索
        :param query_embedding: 查询向量
        :param top_k: 返回数量
        :param filter: 过滤条件
        :return: (文本, 相似度分数) 列表
        """
        search_params = {
            "metric_type": "L2",
            "params": {"ef": 50}
        }
        
        results = self.collection.search(
            data=[query_embedding.tolist()],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=filter,
            output_fields=["text"]
        )
        
        # 转换结果格式，L2距离越小越相似
        hits = []
        for hit in results[0]:
            distance = hit.distance
            text = hit.entity.get("text")
            hits.append((text, 1.0 / (1.0 + distance)))  # 转换为相似度
        
        return hits
    
    def get_collection_stats(self) -> dict:
        """获取集合统计信息"""
        stats = self.collection.stats()
        return {
            "row_count": self.collection.num_entities,
            "index_build": self.collection.has_index("embedding")
        }


# 使用示例
if __name__ == "__main__":
    vector_store = MilvusVectorStore()
    vector_store.connect()
    
    # 创建集合
    vector_store.create_collection("real_estate_knowledge", dimension=768)
    
    # 模拟插入数据
    sample_embeddings = [np.random.rand(768).astype(np.float32) for _ in range(10)]
    sample_texts = [f"文档{i}: 商业地产投资分析..." for i in range(10)]
    sample_sources = ["政策文件", "市场报告"] * 5
    
    vector_store.insert(sample_embeddings, sample_texts, sample_sources)
    
    # 搜索
    query_embedding = np.random.rand(768).astype(np.float32)
    results = vector_store.search(query_embedding, top_k=5)
    
    print("搜索结果:")
    for text, score in results:
        print(f"  相似度: {score:.4f}")
    
    vector_store.disconnect()
```

---

## 七、代码质量与最佳实践

### 问题 7：如何编写可测试的 FastAPI 接口

**参考实现：**

```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyze_investment_success():
    """测试投资分析接口成功案例"""
    response = client.get("/api/v1/investment/analyze", params={
        "city": "上海",
        "property_type": "写字楼",
        "area": 2000
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert data["query"]["city"] == "上海"


def test_analyze_investment_validation_error():
    """测试参数校验失败案例"""
    response = client.get("/api/v1/investment/analyze", params={
        "city": "",  # 空字符串
        "property_type": "住宅"  # 不在允许范围内
    })
    
    assert response.status_code == 422  # Validation Error


def test_analyze_investment_cache():
    """测试缓存功能"""
    # 第一次请求
    response1 = client.get("/api/v1/investment/analyze", params={
        "city": "北京",
        "property_type": "商铺"
    })
    
    # 第二次请求（应该命中缓存）
    response2 = client.get("/api/v1/investment/analyze", params={
        "city": "北京",
        "property_type": "商铺"
    })
    
    assert response1.json() == response2.json()
```

---

## 总结

本文档整理的代码面试题覆盖了商业地产投资分析系统的核心技术实现，包括：

1. **FastAPI 接口开发**：参数校验、依赖注入、异常处理、缓存集成
2. **Redis 会话管理**：分布式会话、数据持久化、过期策略
3. **限流熔断**：Token Bucket 算法、分布式限流
4. **RAG 多路召回**：RRF 融合排序算法
5. **Agent 工具调用**：工具注册、参数校验、结果处理
6. **向量数据库**：Milvus 向量检索封装
7. **测试编写**：API 接口测试最佳实践

这些代码问题考察了候选人的实际编码能力、系统设计能力和对技术栈的理解深度。
