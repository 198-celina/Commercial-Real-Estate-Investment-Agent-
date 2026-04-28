from typing import Dict, Any


class PromptTemplate:
    """商业地产领域提示词模板"""
    
    SYSTEM_PROMPT = """
你是一位专业的商业地产投资分析顾问，精通市场分析、收益测算和风险合规审查。
请基于以下工具返回的信息，为用户提供专业的投资分析建议。

要求：
1. 分析要基于事实数据，引用工具返回的具体指标
2. 语言要专业但易懂，避免使用过于技术化的术语
3. 结构清晰，分点说明，便于用户理解
4. 提供明确的投资建议和风险提示
"""
    
    MARKET_ANALYSIS_TEMPLATE = """
## 商业地产市场分析报告

### 一、市场概况
{market_summary}

### 二、核心指标
| 指标 | 当前值 | 趋势 |
|------|--------|------|
{market_metrics}

### 三、政策影响分析
{policy_analysis}

### 四、市场趋势预测
{trend_prediction}
"""
    
    REVENUE_CALCULATION_TEMPLATE = """
## 投资收益测算报告

### 一、项目基本信息
- 项目名称：{project_name}
- 所在城市：{city}
- 建筑面积：{area}平方米
- 总投资额：{investment}万元

### 二、收益测算
| 指标 | 数值 |
|------|------|
| 月均租金收入 | {monthly_income}万元 |
| 年租金收入 | {annual_income}万元 |
| 年运营费用 | {operating_expenses}万元 |
| 年净收益 | {net_income}万元 |
| 资本化率 | {cap_rate}% |

### 三、投资回报分析
- 投资回收期：{payback_period}年
- 内部收益率(IRR)：{irr}%
- 净现值(NPV)：{npv}万元

### 四、可行性评估
{feasibility_evaluation}
"""
    
    RISK_COMPLIANCE_TEMPLATE = """
## 风险合规评估报告

### 一、合规检查结果
| 检查项 | 状态 | 说明 |
|--------|------|------|
{compliance_items}

### 二、风险识别
| 风险类型 | 等级 | 概率 | 影响 |
|----------|------|------|------|
{risk_items}

### 三、风险总结
{risk_summary}

### 四、合规建议
{compliance_suggestions}
"""
    
    COMBINED_REPORT_TEMPLATE = """
## 商业地产投资综合分析报告

---

### 一、市场分析
{market_section}

---

### 二、收益测算
{revenue_section}

---

### 三、风险合规
{risk_section}

---

### 四、综合投资建议
{investment_suggestion}

---

*报告生成时间：{timestamp}*
"""
    
    def format_market_analysis(self, data: Dict[str, Any]) -> str:
        """格式化市场分析报告"""
        return self.MARKET_ANALYSIS_TEMPLATE.format(
            market_summary=data.get("market_summary", ""),
            market_metrics=data.get("market_metrics", ""),
            policy_analysis=data.get("policy_analysis", ""),
            trend_prediction=data.get("trend_prediction", "")
        )
    
    def format_revenue_calculation(self, data: Dict[str, Any]) -> str:
        """格式化收益测算报告"""
        return self.REVENUE_CALCULATION_TEMPLATE.format(
            project_name=data.get("project_name", "未指定"),
            city=data.get("city", "未指定"),
            area=data.get("area", 0),
            investment=data.get("investment", 0),
            monthly_income=data.get("monthly_income", 0),
            annual_income=data.get("annual_income", 0),
            operating_expenses=data.get("operating_expenses", 0),
            net_income=data.get("net_income", 0),
            cap_rate=data.get("cap_rate", 0),
            payback_period=data.get("payback_period", 0),
            irr=data.get("irr", 0),
            npv=data.get("npv", 0),
            feasibility_evaluation=data.get("feasibility_evaluation", "")
        )
    
    def format_risk_compliance(self, data: Dict[str, Any]) -> str:
        """格式化风险合规报告"""
        return self.RISK_COMPLIANCE_TEMPLATE.format(
            compliance_items=data.get("compliance_items", ""),
            risk_items=data.get("risk_items", ""),
            risk_summary=data.get("risk_summary", ""),
            compliance_suggestions=data.get("compliance_suggestions", "")
        )
    
    def format_combined_report(self, market_data: Dict, revenue_data: Dict, 
                              risk_data: Dict, suggestion: str, 
                              timestamp: str) -> str:
        """格式化综合报告"""
        return self.COMBINED_REPORT_TEMPLATE.format(
            market_section=self.format_market_analysis(market_data),
            revenue_section=self.format_revenue_calculation(revenue_data),
            risk_section=self.format_risk_compliance(risk_data),
            investment_suggestion=suggestion,
            timestamp=timestamp
        )


prompt_template = PromptTemplate()
