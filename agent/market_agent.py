from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from agent.tools.market_tools import MARKET_TOOLS
from agent.tools.rag_tools import RAG_TOOLS
from config.agent_config import agent_config


class MarketAnalysisAgent:
    """市场分析Agent"""
    
    def __init__(self):
        self.name = agent_config.MARKET_AGENT_NAME
        self.description = agent_config.MARKET_AGENT_DESCRIPTION
        self.tools = MARKET_TOOLS + RAG_TOOLS
        self.agent = None  # 延迟初始化
    
    def _initialize_agent(self):
        """初始化Agent"""
        try:
            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.1,
                max_tokens=1024
            )
            # 使用 LangGraph 或简单工具调用
            return {"llm": llm, "tools": self.tools}
        except Exception as e:
            print(f"Warning: Failed to initialize agent: {e}")
            return None
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """执行市场分析"""
        try:
            # 直接调用工具而不是通过 Agent
            results = []
            for tool in self.tools:
                try:
                    if hasattr(tool, '_run'):
                        # 根据工具类型调用
                        if "market" in tool.name.lower():
                            result = tool._run(city="上海", property_type="写字楼")
                            results.append({"tool": tool.name, "result": result})
                except Exception:
                    pass
            
            return {
                "success": True,
                "agent": self.name,
                "result": results,
                "type": "market_analysis"
            }
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "type": "market_analysis"
            }
    
    def get_market_data(self, city: str, area: str = None, property_type: str = "写字楼") -> Dict:
        """获取市场数据"""
        query = f"获取{city}{area or ''}的{property_type}市场行情数据，包括租金水平、空置率、价格走势"
        return self.analyze(query)
    
    def get_policy_info(self, city: str) -> Dict:
        """获取政策信息"""
        query = f"获取{city}最新的房地产政策信息和解读"
        return self.analyze(query)
    
    def get_land_info(self, city: str, land_id: str = None, location: str = None) -> Dict:
        """获取地块信息"""
        query = f"获取{city}{location or ''}的地块信息"
        if land_id:
            query += f"，地块编号：{land_id}"
        return self.analyze(query)
    
    def predict_trend(self, city: str, property_type: str, period: str = "中期") -> Dict:
        """预测市场趋势"""
        query = f"预测{city}{property_type}市场{period}走势"
        return self.analyze(query)
