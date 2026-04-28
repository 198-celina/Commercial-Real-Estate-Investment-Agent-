from typing import List, Dict


class AgentConfig:
    """Agent配置类"""
    
    # 主Agent配置
    MAIN_AGENT_NAME: str = "主调度Agent"
    MAIN_AGENT_DESCRIPTION: str = "负责接收用户请求，分析意图，选择调用垂类Agent，聚合分析结果"
    
    # 垂类Agent配置
    MARKET_AGENT_NAME: str = "市场分析Agent"
    MARKET_AGENT_DESCRIPTION: str = "调取地产行情、政策、地块数据，进行市场趋势分析"
    
    REVENUE_AGENT_NAME: str = "收益测算Agent"
    REVENUE_AGENT_DESCRIPTION: str = "计算租金收益、回报周期、收益率，评估投资可行性"
    
    RISK_AGENT_NAME: str = "风险合规Agent"
    RISK_AGENT_DESCRIPTION: str = "进行政策校验、风险提示、合规审查，识别潜在风险"
    
    # Agent工具列表
    MARKET_TOOLS: List[str] = [
        "get_real_estate_market",
        "get_policy_info",
        "get_land_info",
        "predict_market_trend"
    ]
    
    REVENUE_TOOLS: List[str] = [
        "calculate_rental_income",
        "calculate_payback_period",
        "calculate_irr_npv",
        "evaluate_feasibility"
    ]
    
    RISK_TOOLS: List[str] = [
        "check_policy_compliance",
        "identify_risk_points",
        "generate_risk_report",
        "get_compliance_suggestions"
    ]
    
    # 调用策略
    CALL_TIMEOUT: int = 60  # 工具调用超时时间（秒）
    MAX_RETRY: int = 3      # 最大重试次数
    
    # 意图识别关键词映射
    INTENT_KEYWORDS: Dict[str, List[str]] = {
        "market_analysis": ["市场", "行情", "政策", "地块", "趋势", "动态"],
        "revenue_calculation": ["收益", "租金", "回报", "测算", "IRR", "NPV", "可行性"],
        "risk_compliance": ["风险", "合规", "审查", "政策", "校验", "提示"]
    }


agent_config = AgentConfig()
