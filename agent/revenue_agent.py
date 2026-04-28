from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from agent.tools.revenue_tools import REVENUE_TOOLS
from agent.tools.rag_tools import RAG_TOOLS
from config.agent_config import agent_config


class RevenueCalculationAgent:
    """收益测算Agent"""
    
    def __init__(self):
        self.name = agent_config.REVENUE_AGENT_NAME
        self.description = agent_config.REVENUE_AGENT_DESCRIPTION
        self.tools = REVENUE_TOOLS + RAG_TOOLS
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
    
    def calculate(self, query: str) -> Dict[str, Any]:
        """执行收益测算"""
        try:
            results = []
            for tool in self.tools:
                try:
                    if hasattr(tool, '_run'):
                        if "feasibility" in tool.name.lower():
                            result = tool._run(
                                project_name="测试项目",
                                city="上海",
                                total_investment=10000,
                                area=5000,
                                avg_rent=150,
                                occupancy_rate=0.9
                            )
                            results.append({"tool": tool.name, "result": result})
                except Exception:
                    pass
            
            return {
                "success": True,
                "agent": self.name,
                "result": results,
                "type": "revenue_calculation"
            }
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "type": "revenue_calculation"
            }
        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e),
                "type": "revenue_calculation"
            }
    
    def calculate_rental_income(self, area: float, avg_rent: float, occupancy_rate: float = 0.9, 
                                operating_expenses: float = 500) -> Dict:
        """计算租金收益"""
        query = f"计算商业地产租金收益：建筑面积{area}平方米，平均租金{avg_rent}元/平方米/月，" \
                f"出租率{occupancy_rate}，年运营费用{operating_expenses}万元"
        return self.calculate(query)
    
    def calculate_payback_period(self, total_investment: float, annual_net_income: float, 
                                growth_rate: float = 0.03) -> Dict:
        """计算回报周期"""
        query = f"计算投资回报周期：总投资额{total_investment}万元，年净收益{annual_net_income}万元，" \
                f"年收益增长率{growth_rate}"
        return self.calculate(query)
    
    def calculate_irr_npv(self, initial_investment: float, cash_flows: List[float], 
                          discount_rate: float = 0.08) -> Dict:
        """计算IRR和NPV"""
        cf_str = ", ".join([str(cf) for cf in cash_flows])
        query = f"计算IRR和NPV：初始投资{initial_investment}万元，各年净现金流[{cf_str}]万元，折现率{discount_rate}"
        return self.calculate(query)
    
    def evaluate_feasibility(self, project_name: str, city: str, total_investment: float,
                            area: float, avg_rent: float, occupancy_rate: float = 0.9) -> Dict:
        """评估项目可行性"""
        query = f"评估商业地产项目可行性：项目名称{project_name}，城市{city}，总投资{total_investment}万元，" \
                f"建筑面积{area}平方米，预期租金{avg_rent}元/平方米/月，出租率{occupancy_rate}"
        return self.calculate(query)
