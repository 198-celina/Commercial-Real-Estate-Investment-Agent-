from typing import Dict, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class CalculateRentalIncomeInput(BaseModel):
    """租金收益计算输入参数"""
    area: float = Field(description="建筑面积（平方米）")
    avg_rent: float = Field(description="平均租金（元/平方米/月）")
    occupancy_rate: float = Field(description="出租率，范围0-1")
    operating_expenses: float = Field(description="运营费用（万元/年）")


class CalculateRentalIncomeTool(BaseTool):
    name: str = "calculate_rental_income"
    description: str = "计算商业地产项目的租金收益"
    args_schema: type = CalculateRentalIncomeInput
    
    def _run(self, area: float, avg_rent: float, occupancy_rate: float = 0.9, operating_expenses: float = 500) -> Dict:
        """执行租金收益计算"""
        monthly_income = area * avg_rent * occupancy_rate
        annual_income = monthly_income * 12 / 10000  # 转换为万元
        net_annual_income = annual_income - operating_expenses
        
        return {
            "input_params": {
                "area": area,
                "avg_rent": avg_rent,
                "occupancy_rate": occupancy_rate,
                "operating_expenses": operating_expenses
            },
            "monthly_gross_income": round(monthly_income, 2),
            "annual_gross_income": round(annual_income, 2),
            "annual_operating_expenses": operating_expenses,
            "annual_net_income": round(net_annual_income, 2),
            "yield_rate": round(net_annual_income / (area * avg_rent * 12 / 10000) * 100, 2)
        }


class CalculatePaybackPeriodInput(BaseModel):
    """回报周期计算输入参数"""
    total_investment: float = Field(description="总投资额（万元）")
    annual_net_income: float = Field(description="年净收益（万元）")
    growth_rate: float = Field(description="年收益增长率，范围0-1")


class CalculatePaybackPeriodTool(BaseTool):
    name: str = "calculate_payback_period"
    description: str = "计算投资回报周期"
    args_schema: type = CalculatePaybackPeriodInput
    
    def _run(self, total_investment: float, annual_net_income: float, growth_rate: float = 0.03) -> Dict:
        """执行回报周期计算"""
        years = 0
        cumulative_income = 0
        current_income = annual_net_income
        
        while cumulative_income < total_investment:
            cumulative_income += current_income
            current_income *= (1 + growth_rate)
            years += 1
        
        return {
            "total_investment": total_investment,
            "initial_annual_income": annual_net_income,
            "growth_rate": growth_rate,
            "payback_period_years": years,
            "discounted_payback_period": round(years * 1.15, 1),
            "analysis": f"投资回报周期约为{years}年，考虑资金时间价值后约为{round(years * 1.15, 1)}年"
        }


class CalculateIRRNPVInput(BaseModel):
    """IRR和NPV计算输入参数"""
    initial_investment: float = Field(description="初始投资（万元）")
    cash_flows: list = Field(description="各年净现金流（万元），按年度顺序")
    discount_rate: float = Field(description="折现率，范围0-1")


class CalculateIRRNPVTool(BaseTool):
    name: str = "calculate_irr_npv"
    description: str = "计算内部收益率(IRR)和净现值(NPV)"
    args_schema: type = CalculateIRRNPVInput
    
    def _run(self, initial_investment: float, cash_flows: list, discount_rate: float = 0.08) -> Dict:
        """执行IRR和NPV计算"""
        # 简化的IRR计算
        npv = -initial_investment
        for i, cf in enumerate(cash_flows):
            npv += cf / (1 + discount_rate) ** (i + 1)
        
        # 简化IRR估算
        irr = 0.0
        for rate in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
            temp_npv = -initial_investment
            for i, cf in enumerate(cash_flows):
                temp_npv += cf / (1 + rate) ** (i + 1)
            if temp_npv >= 0:
                irr = rate
        
        return {
            "initial_investment": initial_investment,
            "cash_flows": cash_flows,
            "discount_rate": discount_rate,
            "npv": round(npv, 2),
            "irr": round(irr * 100, 2),
            "analysis": {
                "npv_status": "positive" if npv > 0 else "negative",
                "irr_status": "good" if irr > discount_rate else "poor",
                "recommendation": "项目可行" if (npv > 0 and irr > discount_rate) else "需谨慎评估"
            }
        }


class EvaluateFeasibilityInput(BaseModel):
    """可行性评估输入参数"""
    project_name: str = Field(description="项目名称")
    city: str = Field(description="所在城市")
    total_investment: float = Field(description="总投资额（万元）")
    area: float = Field(description="建筑面积（平方米）")
    avg_rent: float = Field(description="预期租金（元/平方米/月）")
    occupancy_rate: float = Field(description="预期出租率")


class EvaluateFeasibilityTool(BaseTool):
    name: str = "evaluate_feasibility"
    description: str = "综合评估商业地产投资项目可行性"
    args_schema: type = EvaluateFeasibilityInput
    
    def _run(self, project_name: str, city: str, total_investment: float, 
             area: float, avg_rent: float, occupancy_rate: float = 0.9) -> Dict:
        """执行可行性评估"""
        # 计算关键指标
        monthly_income = area * avg_rent * occupancy_rate
        annual_income = monthly_income * 12 / 10000
        operating_expenses = total_investment * 0.03  # 假设运营费用为投资的3%
        net_income = annual_income - operating_expenses
        cap_rate = net_income / total_investment * 100
        
        # 评估等级
        if cap_rate >= 8:
            grade = "A"
            status = "优秀"
        elif cap_rate >= 6:
            grade = "B"
            status = "良好"
        elif cap_rate >= 4:
            grade = "C"
            status = "一般"
        else:
            grade = "D"
            status = "较差"
        
        return {
            "project_name": project_name,
            "city": city,
            "total_investment": total_investment,
            "area": area,
            "key_metrics": {
                "annual_gross_income": round(annual_income, 2),
                "annual_operating_expenses": round(operating_expenses, 2),
                "annual_net_income": round(net_income, 2),
                "cap_rate": round(cap_rate, 2),
                "payback_period": round(total_investment / net_income, 1)
            },
            "evaluation": {
                "grade": grade,
                "status": status,
                "summary": f"{project_name}位于{city}，总投资{total_investment}万元，建筑面积{area}平方米。"
                          f"预期年净收益{round(net_income, 2)}万元，资本化率{round(cap_rate, 2)}%，"
                          f"投资回报周期约{round(total_investment / net_income, 1)}年。"
                          f"综合评估：{status}({grade}级)"
            }
        }


# 收益测算工具列表
REVENUE_TOOLS = [
    CalculateRentalIncomeTool(),
    CalculatePaybackPeriodTool(),
    CalculateIRRNPVTool(),
    EvaluateFeasibilityTool()
]
