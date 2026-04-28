from typing import List, Dict
from collections import defaultdict


class RRFReRanker:
    """RRF(Reciprocal Rank Fusion)重排器"""
    
    def __init__(self, k: int = 60):
        """
        Args:
            k: RRF参数，默认60
        """
        self.k = k
    
    def rerank(self, candidates: List[Dict], top_k: int = 10) -> List[Dict]:
        """
        使用RRF算法对多路召回结果进行重排
        
        Args:
            candidates: 候选文档列表，每个文档包含score字段
            top_k: 返回前k个结果
        
        Returns:
            重排后的文档列表
        """
        if not candidates:
            return []
        
        # 按分数排序获取排名
        sorted_candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)
        
        # 计算RRF分数
        rrf_scores = {}
        for rank, doc in enumerate(sorted_candidates, 1):
            doc_id = doc.get("id", doc.get("title", str(id(doc))))
            rrf_score = 1 / (self.k + rank)
            
            if doc_id in rrf_scores:
                rrf_scores[doc_id] += rrf_score
            else:
                rrf_scores[doc_id] = rrf_score
        
        # 按RRF分数排序
        doc_map = {doc.get("id", doc.get("title", str(id(doc)))): doc for doc in sorted_candidates}
        reranked = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 返回结果
        results = []
        for doc_id, score in reranked[:top_k]:
            doc = doc_map.get(doc_id)
            if doc:
                doc["rrf_score"] = round(score, 4)
                results.append(doc)
        
        return results


rrf_reranker = RRFReRanker()
