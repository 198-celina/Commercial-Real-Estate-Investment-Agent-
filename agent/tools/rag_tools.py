from typing import Dict, List
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from rag.retriever import MultiRetriever
from rag.rrf_reranker import RRFReRanker


class RetrieveKnowledgeInput(BaseModel):
    """知识检索输入参数"""
    query: str = Field(description="用户查询问题")
    top_k: int = Field(description="返回结果数量", ge=1, le=20)


class RetrieveKnowledgeTool(BaseTool):
    name: str = "retrieve_knowledge"
    description: str = "从商业地产知识库中检索相关信息"
    args_schema: type = RetrieveKnowledgeInput
    
    def _run(self, query: str, top_k: int = 10) -> Dict:
        """执行知识检索"""
        # 初始化检索器和重排器
        retriever = MultiRetriever()
        reranker = RRFReRanker()
        
        # 多路召回
        candidates = retriever.multi_retrieve(query, top_k=top_k * 2)
        
        # RRF重排
        reranked_results = reranker.rerank(candidates, top_k=top_k)
        
        # 格式化结果
        results = []
        for item in reranked_results:
            results.append({
                "title": item.get("title", ""),
                "content": item.get("content", "")[:500] + "..." if len(item.get("content", "")) > 500 else item.get("content", ""),
                "source": item.get("source", "unknown"),
                "category": item.get("category", ""),
                "relevance_score": round(item.get("score", 0), 4)
            })
        
        return {
            "query": query,
            "total_results": len(results),
            "results": results,
            "summary": f"从知识库中检索到{len(results)}条相关信息，已按相关性排序"
        }


class QueryPolicyKnowledgeInput(BaseModel):
    """政策知识查询输入参数"""
    query: str = Field(description="政策查询问题")
    city: str = Field(description="目标城市")


class QueryPolicyKnowledgeTool(BaseTool):
    name: str = "query_policy_knowledge"
    description: str = "查询商业地产政策相关知识"
    args_schema: type = QueryPolicyKnowledgeInput
    
    def _run(self, query: str, city: str) -> Dict:
        """执行政策知识查询"""
        retriever = MultiRetriever()
        reranker = RRFReRanker()
        
        # 构建查询
        full_query = f"{city} {query}"
        candidates = retriever.multi_retrieve(full_query, top_k=15)
        
        # 过滤政策相关内容
        policy_candidates = [c for c in candidates if c.get("category") == "policy"]
        if not policy_candidates:
            policy_candidates = candidates
        
        reranked_results = reranker.rerank(policy_candidates, top_k=5)
        
        results = []
        for item in reranked_results:
            results.append({
                "title": item.get("title", ""),
                "content": item.get("content", "")[:800] + "..." if len(item.get("content", "")) > 800 else item.get("content", ""),
                "source": item.get("source", "unknown"),
                "relevance_score": round(item.get("score", 0), 4)
            })
        
        return {
            "city": city,
            "query": query,
            "policy_results": results,
            "summary": f"查询到{len(results)}条与{city}相关的政策信息"
        }


# RAG工具列表
RAG_TOOLS = [
    RetrieveKnowledgeTool(),
    QueryPolicyKnowledgeTool()
]
