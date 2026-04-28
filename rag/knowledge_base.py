from typing import List, Dict, Optional
from rag.vector_store import vector_store
from config.milvus_config import milvus_config


class KnowledgeBase:
    """知识库管理类"""
    
    def __init__(self):
        self.vector_store = vector_store
    
    def add_document(self, content: str, title: str, source: str, 
                     category: str, embedding: Optional[List[float]] = None) -> bool:
        """添加文档到知识库"""
        try:
            if embedding is None:
                # 实际应调用嵌入模型生成向量
                embedding = [0.0] * 768
            
            self.vector_store.insert(
                embeddings=[embedding],
                contents=[content],
                titles=[title],
                sources=[source],
                categories=[category]
            )
            return True
        except Exception as e:
            print(f"Failed to add document: {e}")
            return False
    
    def add_documents(self, documents: List[Dict]) -> int:
        """批量添加文档"""
        if not documents:
            return 0
        
        embeddings = []
        contents = []
        titles = []
        sources = []
        categories = []
        
        for doc in documents:
            embeddings.append(doc.get("embedding", [0.0] * 768))
            contents.append(doc["content"])
            titles.append(doc.get("title", ""))
            sources.append(doc.get("source", "unknown"))
            categories.append(doc.get("category", "general"))
        
        try:
            return self.vector_store.insert(embeddings, contents, titles, sources, categories)
        except Exception as e:
            print(f"Failed to add documents: {e}")
            return 0
    
    def search(self, query_embedding: List[float], top_k: int = 10) -> List[Dict]:
        """搜索知识库"""
        return self.vector_store.search(query_embedding, top_k=top_k)
    
    def get_by_category(self, category: str, limit: int = 100) -> List[Dict]:
        """按类别获取文档"""
        filter_expr = f'category == "{category}"'
        return self.vector_store.query(filter_expr)[:limit]
    
    def delete_by_source(self, source: str) -> int:
        """按来源删除文档"""
        filter_expr = f'source == "{source}"'
        return self.vector_store.delete(filter_expr)
    
    def get_stats(self) -> Dict:
        """获取知识库统计信息"""
        return {
            "total_documents": self.vector_store.count(),
            "collection_name": milvus_config.COLLECTION_NAME,
            "dimension": milvus_config.DIMENSION
        }
    
    def clear(self) -> bool:
        """清空知识库"""
        try:
            milvus_config.create_collection(overwrite=True)
            return True
        except Exception as e:
            print(f"Failed to clear knowledge base: {e}")
            return False


knowledge_base = KnowledgeBase()
