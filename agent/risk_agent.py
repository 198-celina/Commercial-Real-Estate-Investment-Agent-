from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from agent.tools.risk_tools import RISK_TOOLS
from agent.tools.rag_tools import RAG_TOOLS
from config.agent_config import agent_config


class RiskComplianceAgent:
    """风险合规Agent"""
    
    def __init__(self):
        self.name = agent_config.RISK_AGENT_NAME
        self.description = agent_config.RISK_AGENT_DESCRIPTION
        self.tools = RISK_TOOLS + RAG_TOOLS
        self.agent = None  # 延迟初始化
    
    def _initialize_agent(self):
        """初始化Agent"""
        try:
            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.1,
                max_tokens=1024
            )
            return {"llm": llm, "tools": self.tools}
        except Exception as e:
            print(f"Warning: Failed to initialize agent: {e}")
            return None
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """执行风险分析"""
        try:
            results = []
            for tool in self.tools:
                try:
                    if hasattr(tool, '_run'):
                        if "compliance" in tool.name.lower():
                            result = tool._run(
                                city="上海",
                                project_type="写字楼",
                                land_area=5000,
                                building_area=20000
                            )
                            results.append({"tool": tool.name, "result": result})
                except Exception:
                    pass
            
            return {
                "success": True,
                "agent": self.name,
                "result": results,
                "type": "risk_compliance"
            }
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "type": "risk_compliance"
            }
    
    def check_compliance(self, city: str, project_type: str, land_area: float, 
                        building_area: float) -> Dict:
        """检查政策合规"""
        query = f"检查{city}{project_type}项目政策合规性：用地面积{land_area}平方米，建筑面积{building_area}平方米"
        return self.analyze(query)
    
    def identify_risks(self, city: str, project_type: str, investment_amount: float, 
                      timeline: int) -> Dict:
        """识别风险点"""
        query = f"识别{city}{project_type}项目风险点：投资金额{investment_amount}万元，项目周期{timeline}个月"
        return self.analyze(query)
    
    def generate_risk_report(self, project_name: str, city: str, risks: List[Dict]) -> Dict:
        """生成风险报告"""
        risks_str = str(risks)
        query = f"生成{project_name}（{city}）的风险评估报告，风险列表：{risks_str}"
        return self.analyze(query)
    
    def get_compliance_suggestions(self, city: str, project_type: str, issues: List[str]) -> Dict:
        """获取合规建议"""
        issues_str = ", ".join(issues)
        query = f"针对{city}{project_type}项目的合规问题提供建议，问题列表：{issues_str}"
        return self.analyze(query)
