from typing import List, Dict
from rag.vector_store import vector_store


class MultiRetriever:
    """多路召回检索器"""
    
    def __init__(self):
        self.vector_store = vector_store
    
    def _vector_retrieve(self, query_embedding: List[float], top_k: int = 10) -> List[Dict]:
        """向量检索"""
        return self.vector_store.search(query_embedding, top_k=top_k)
    
    def _keyword_retrieve(self, query: str, top_k: int = 10) -> List[Dict]:
        """关键词检索（模拟BM25）"""
        # 简化实现：基于标题和内容的关键词匹配
        results = []
        
        # 这里应该调用实际的关键词检索引擎（如Elasticsearch）
        # 以下是模拟实现
        mock_results = [
            {"title": f"关于{query}的政策解读", "content": "政策内容...", "source": "政府官网", "category": "policy", "score": 0.8},
            {"title": f"{query}市场分析报告", "content": "市场数据...", "source": "行业报告", "category": "market", "score": 0.7},
            {"title": f"{query}投资指南", "content": "投资建议...", "source": "咨询机构", "category": "investment", "score": 0.6}
        ]
        
        return mock_results[:top_k]
    
    def _semantic_retrieve(self, query: str, top_k: int = 10) -> List[Dict]:
        """语义相似度检索"""
        # 简化实现：模拟语义匹配结果
        mock_results = [
            {"title": f"{query}相关分析", "content": "语义匹配内容...", "source": "知识库", "category": "analysis", "score": 0.85},
            {"title": f"{query}深度研究", "content": "研究报告内容...", "source": "研究机构", "category": "research", "score": 0.75}
        ]
        
        return mock_results[:top_k]
    
    def multi_retrieve(self, query: str, query_embedding: List[float] = None, top_k: int = 10) -> List[Dict]:
        """多路召回"""
        # 如果没有提供向量，使用空向量（实际应调用嵌入模型）
        if query_embedding is None:
            query_embedding = [0.0] * 768
        
        # 三路召回
        vector_results = self._vector_retrieve(query_embedding, top_k=top_k)
        keyword_results = self._keyword_retrieve(query, top_k=top_k)
        semantic_results = self._semantic_retrieve(query, top_k=top_k)
        
        # 合并结果，去重
        all_results = []
        seen_ids = set()
        
        for result in vector_results + keyword_results + semantic_results:
            result_id = result.get("id", result.get("title", ""))
            if result_id not in seen_ids:
                seen_ids.add(result_id)
                all_results.append(result)
        
        return all_results[:top_k * 2]  # 返回双倍数量供重排


multi_retriever = MultiRetriever()
