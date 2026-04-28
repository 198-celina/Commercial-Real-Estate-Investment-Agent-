from typing import Dict, List, Any
from agent.market_agent import MarketAnalysisAgent
from agent.revenue_agent import RevenueCalculationAgent
from agent.risk_agent import RiskComplianceAgent
from config.agent_config import agent_config


class MainAgent:
    """主调度Agent"""
    
    def __init__(self):
        self.name = agent_config.MAIN_AGENT_NAME
        self.description = agent_config.MAIN_AGENT_DESCRIPTION
        self.market_agent = MarketAnalysisAgent()
        self.revenue_agent = RevenueCalculationAgent()
        self.risk_agent = RiskComplianceAgent()
    
    def _identify_intent(self, query: str) -> List[str]:
        """识别用户意图"""
        intents = []
        keywords = agent_config.INTENT_KEYWORDS
        
        for intent, kw_list in keywords.items():
            for kw in kw_list:
                if kw in query:
                    intents.append(intent)
                    break
        
        # 如果没有识别到具体意图，默认进行综合分析
        if not intents:
            intents = ["market_analysis", "revenue_calculation", "risk_compliance"]
        
        return list(set(intents))
    
    def _dispatch_task(self, intent: str, query: str) -> Dict[str, Any]:
        """任务分发"""
        dispatch_map = {
            "market_analysis": self.market_agent.analyze,
            "revenue_calculation": self.revenue_agent.calculate,
            "risk_compliance": self.risk_agent.analyze
        }
        
        handler = dispatch_map.get(intent)
        if handler:
            return handler(query)
        return {"success": False, "error": f"Unknown intent: {intent}"}
    
    def _aggregate_results(self, results: List[Dict]) -> Dict[str, Any]:
        """结果聚合"""
        successful_results = [r for r in results if r.get("success")]
        failed_results = [r for r in results if not r.get("success")]
        
        aggregated = {
            "total_tasks": len(results),
            "successful_tasks": len(successful_results),
            "failed_tasks": len(failed_results),
            "results": {},
            "summary": ""
        }
        
        # 按类型组织结果
        for result in successful_results:
            result_type = result.get("type", "unknown")
            aggregated["results"][result_type] = result
        
        # 生成总结
        summaries = []
        if "market_analysis" in aggregated["results"]:
            summaries.append("市场分析已完成")
        if "revenue_calculation" in aggregated["results"]:
            summaries.append("收益测算已完成")
        if "risk_compliance" in aggregated["results"]:
            summaries.append("风险合规审查已完成")
        
        if failed_results:
            summaries.append(f"部分任务失败（{len(failed_results)}项）")
        
        aggregated["summary"] = "；".join(summaries)
        
        return aggregated
    
    def run(self, query: str) -> Dict[str, Any]:
        """执行主流程"""
        # 1. 意图识别
        intents = self._identify_intent(query)
        
        # 2. 任务分发与执行
        results = []
        for intent in intents:
            result = self._dispatch_task(intent, query)
            results.append(result)
        
        # 3. 结果聚合
        aggregated = self._aggregate_results(results)
        
        # 4. 生成最终响应
        final_response = {
            "success": aggregated["successful_tasks"] > 0,
            "intents": intents,
            "agent": self.name,
            "analysis_results": aggregated["results"],
            "summary": aggregated["summary"]
        }
        
        return final_response
    
    def get_agent_info(self) -> Dict:
        """获取Agent信息"""
        return {
            "name": self.name,
            "description": self.description,
            "sub_agents": [
                {
                    "name": self.market_agent.name,
                    "description": self.market_agent.description,
                    "tools": [t.name for t in self.market_agent.tools]
                },
                {
                    "name": self.revenue_agent.name,
                    "description": self.revenue_agent.description,
                    "tools": [t.name for t in self.revenue_agent.tools]
                },
                {
                    "name": self.risk_agent.name,
                    "description": self.risk_agent.description,
                    "tools": [t.name for t in self.risk_agent.tools]
                }
            ]
        }
