from fastapi import APIRouter, HTTPException
from api.v1.schemas.request import InvestmentAnalysisRequest
from api.v1.schemas.response import InvestmentAnalysisResponse
from agent.market_agent import MarketAnalysisAgent
from agent.revenue_agent import RevenueCalculationAgent
from agent.risk_agent import RiskComplianceAgent
from session.session_manager import session_manager

router = APIRouter(prefix="/investment", tags=["投资分析"])

market_agent = MarketAnalysisAgent()
revenue_agent = RevenueCalculationAgent()
risk_agent = RiskComplianceAgent()


@router.post("/analyze", response_model=InvestmentAnalysisResponse)
async def analyze_investment(request: InvestmentAnalysisRequest):
    """投资分析接口"""
    try:
        # 检查会话
        if not request.session_id or not session_manager.exists(request.session_id):
            session_id = session_manager.create_session()
        else:
            session_id = request.session_id
        
        result = {
            "session_id": session_id,
            "success": True,
            "market_analysis": None,
            "revenue_calculation": None,
            "risk_compliance": None,
            "summary": ""
        }
        
        analysis_type = request.analysis_type
        
        # 根据分析类型调用相应的Agent
        if analysis_type in ["market", "comprehensive"]:
            market_result = market_agent.analyze(
                f"分析{request.city}的{request.property_type}市场行情和政策"
            )
            result["market_analysis"] = market_result
        
        if analysis_type in ["revenue", "comprehensive"]:
            revenue_result = revenue_agent.evaluate_feasibility(
                project_name=request.project_name or "未命名项目",
                city=request.city,
                total_investment=request.investment_amount or 10000,
                area=request.area or 10000,
                avg_rent=150,  # 默认租金
                occupancy_rate=0.9
            )
            result["revenue_calculation"] = revenue_result
        
        if analysis_type in ["risk", "comprehensive"]:
            risk_result = risk_agent.analyze(
                f"分析{request.city}{request.property_type}项目的风险合规情况，"
                f"投资金额{request.investment_amount or 10000}万元"
            )
            result["risk_compliance"] = risk_result
        
        # 生成摘要
        summaries = []
        if result["market_analysis"]:
            summaries.append("市场分析完成")
        if result["revenue_calculation"]:
            summaries.append("收益测算完成")
        if result["risk_compliance"]:
            summaries.append("风险合规审查完成")
        
        result["summary"] = "；".join(summaries)
        
        return InvestmentAnalysisResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/{city}")
async def get_market_analysis(city: str, area: str = None):
    """获取市场分析"""
    try:
        result = market_agent.get_market_data(city, area)
        return {"city": city, "area": area, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/revenue/calculate")
async def calculate_revenue(area: float, avg_rent: float, investment: float):
    """计算投资收益"""
    try:
        result = revenue_agent.evaluate_feasibility(
            project_name="计算项目",
            city="未指定",
            total_investment=investment,
            area=area,
            avg_rent=avg_rent
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk/{city}")
async def get_risk_analysis(city: str, property_type: str = "写字楼"):
    """获取风险分析"""
    try:
        result = risk_agent.analyze(f"分析{city}{property_type}项目的风险合规情况")
        return {"city": city, "property_type": property_type, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
