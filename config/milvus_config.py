from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)
from config.settings import settings
import os


class MilvusConfig:
    """Milvus向量库配置类（支持 Milvus Lite）"""
    
    # 连接配置
    HOST = settings.MILVUS_HOST
    PORT = settings.MILVUS_PORT
    COLLECTION_NAME = settings.MILVUS_COLLECTION_NAME
    DIMENSION = settings.MILVUS_DIMENSION
    
    # Milvus Lite 配置
    LITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "milvus_lite.db")
    
    # 索引配置
    INDEX_TYPE = "HNSW"
    METRIC_TYPE = "IP"  # Inner Product
    INDEX_PARAMS = {
        "M": 16,
        "efConstruction": 200,
        "ef": 64
    }
    
    # 字段定义
    FIELDS = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=128),
        FieldSchema(name="timestamp", dtype=DataType.INT64)
    ]
    
    # 查询参数
    TOP_K = 10
    NPROBE = 10
    
    @classmethod
    def connect(cls):
        """建立Milvus连接（使用 Milvus Lite）"""
        try:
            # 直接使用 Milvus Lite
            os.makedirs(os.path.dirname(cls.LITE_DB_PATH), exist_ok=True)
            from milvus import default_server
            default_server.start()
            cls._lite_client = default_server
            connections.connect(
                alias="default",
                host="127.0.0.1",
                port=str(default_server.listen_port)
            )
            print(f"Connected to Milvus Lite at 127.0.0.1:{default_server.listen_port}")
        except Exception as e:
            print(f"Milvus Lite connection failed: {e}")
            raise
    
    @classmethod
    def create_collection(cls, overwrite: bool = False):
        """创建向量集合"""
        if utility.has_collection(cls.COLLECTION_NAME):
            if overwrite:
                utility.drop_collection(cls.COLLECTION_NAME)
            else:
                return
        
        schema = CollectionSchema(fields=cls.FIELDS, description="商业地产投资知识库")
        collection = Collection(name=cls.COLLECTION_NAME, schema=schema)
        
        # 创建索引
        collection.create_index(
            field_name="embedding",
            index_params={
                "metric_type": cls.METRIC_TYPE,
                "index_type": cls.INDEX_TYPE,
                "params": cls.INDEX_PARAMS
            }
        )
        
        return collection
    
    @classmethod
    def get_collection(cls) -> Collection:
        """获取集合对象"""
        return Collection(name=cls.COLLECTION_NAME)


milvus_config = MilvusConfig()
