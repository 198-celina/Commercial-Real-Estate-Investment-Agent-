from typing import List, Dict, Optional
from pymilvus import Collection, connections, utility
from config.milvus_config import milvus_config


class VectorStore:
    """Milvus向量库操作封装"""
    
    def __init__(self):
        self._connect()
        self.collection = None
        try:
            # 尝试获取现有集合
            if utility.has_collection(milvus_config.COLLECTION_NAME):
                self.collection = milvus_config.get_collection()
            else:
                # 创建新集合
                self.collection = milvus_config.create_collection()
                if self.collection:
                    self.collection.load()
        except Exception as e:
            print(f"Warning: Failed to initialize collection: {e}")
    
    def _connect(self):
        """建立Milvus连接"""
        try:
            milvus_config.connect()
        except Exception as e:
            print(f"Warning: Failed to connect to Milvus: {e}")
            # 不抛出异常，允许在没有 Milvus 的情况下运行
    
    def insert(self, embeddings: List[List[float]], contents: List[str], 
               titles: List[str], sources: List[str], categories: List[str]) -> int:
        """插入向量数据"""
        try:
            entities = [
                embeddings,
                contents,
                titles,
                sources,
                categories,
                [0] * len(embeddings)  # timestamp placeholder
            ]
            
            self.collection.insert(entities)
            self.collection.flush()
            return len(embeddings)
        except Exception as e:
            raise RuntimeError(f"Failed to insert data: {e}")
    
    def search(self, query_embedding: List[float], top_k: int = 10) -> List[Dict]:
        """向量检索"""
        try:
            self.collection.load()
            
            search_params = {
                "metric_type": milvus_config.METRIC_TYPE,
                "params": {"nprobe": milvus_config.NPROBE}
            }
            
            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["content", "title", "source", "category"]
            )
            
            search_results = []
            for hit in results[0]:
                search_results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "content": hit.entity.get("content"),
                    "title": hit.entity.get("title"),
                    "source": hit.entity.get("source"),
                    "category": hit.entity.get("category")
                })
            
            return search_results
        except Exception as e:
            raise RuntimeError(f"Failed to search: {e}")
    
    def query(self, filter_expr: str, output_fields: Optional[List[str]] = None) -> List[Dict]:
        """标量查询"""
        try:
            self.collection.load()
            
            if output_fields is None:
                output_fields = ["content", "title", "source", "category"]
            
            results = self.collection.query(
                expr=filter_expr,
                output_fields=output_fields
            )
            
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to query: {e}")
    
    def delete(self, expr: str) -> int:
        """删除数据"""
        try:
            result = self.collection.delete(expr)
            self.collection.flush()
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to delete: {e}")
    
    def count(self) -> int:
        """统计数据量"""
        try:
            return self.collection.num_entities
        except Exception as e:
            raise RuntimeError(f"Failed to count: {e}")
    
    def create_index(self):
        """创建索引"""
        try:
            self.collection.create_index(
                field_name="embedding",
                index_params={
                    "metric_type": milvus_config.METRIC_TYPE,
                    "index_type": milvus_config.INDEX_TYPE,
                    "params": milvus_config.INDEX_PARAMS
                }
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create index: {e}")


vector_store = VectorStore()
