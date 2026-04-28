from typing import Dict, List, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class CheckPolicyComplianceInput(BaseModel):
    """政策合规检查输入参数"""
    city: str = Field(description="城市名称")
    project_type: str = Field(description="项目类型：写字楼、商铺、住宅等")
    land_area: float = Field(description="用地面积（平方米）")
    building_area: float = Field(description="建筑面积（平方米）")


class CheckPolicyComplianceTool(BaseTool):
    name: str = "check_policy_compliance"
    description: str = "检查项目是否符合当地房地产政策要求"
    args_schema: type = CheckPolicyComplianceInput
    
    def _run(self, city: str, project_type: str, land_area: float, building_area: float) -> Dict:
        """执行政策合规检查"""
        far = building_area / land_area
        compliance_items = []
        
        # 模拟政策检查
        if far > 6.0:
            compliance_items.append({
                "item": "容积率",
                "status": "warning",
                "message": f"容积率{far:.2f}超过当地上限6.0，可能需要调整规划"
            })
        else:
            compliance_items.append({
                "item": "容积率",
                "status": "pass",
                "message": f"容积率{far:.2f}符合要求"
            })
        
        if project_type == "写字楼" and building_area < 5000:
            compliance_items.append({
                "item": "最小建筑面积",
                "status": "warning",
                "message": "写字楼项目建筑面积低于5000平方米最低要求"
            })
        else:
            compliance_items.append({
                "item": "最小建筑面积",
                "status": "pass",
                "message": "建筑面积符合要求"
            })
        
        compliance_items.append({
            "item": "土地用途",
            "status": "pass",
            "message": f"{project_type}项目用地性质符合规划"
        })
        
        compliance_items.append({
            "item": "配套设施",
            "status": "pass",
            "message": "配套设施比例符合当地规定"
        })
        
        overall_status = "compliant" if all(item["status"] == "pass" for item in compliance_items) else "conditional"
        
        return {
            "city": city,
            "project_type": project_type,
            "compliance_checks": compliance_items,
            "overall_status": overall_status,
            "summary": f"{city}{project_type}项目政策合规检查{'通过' if overall_status == 'compliant' else '基本通过，部分事项需关注'}"
        }


class IdentifyRiskPointsInput(BaseModel):
    """风险识别输入参数"""
    city: str = Field(description="城市名称")
    project_type: str = Field(description="项目类型")
    investment_amount: float = Field(description="投资金额（万元）")
    timeline: int = Field(description="项目周期（月）")


class IdentifyRiskPointsTool(BaseTool):
    name: str = "identify_risk_points"
    description: str = "识别商业地产投资项目的潜在风险点"
    args_schema: type = IdentifyRiskPointsInput
    
    def _run(self, city: str, project_type: str, investment_amount: float, timeline: int) -> Dict:
        """执行风险识别"""
        risks = []
        
        # 政策风险
        risks.append({
            "category": "政策风险",
            "level": "medium",
            "description": "房地产调控政策可能变化，影响项目审批和销售",
            "probability": 0.4,
            "impact": "high",
            "mitigation": "密切关注政策动态，预留政策调整应对时间"
        })
        
        # 市场风险
        risks.append({
            "category": "市场风险",
            "level": "medium",
            "description": f"{city}商业地产供应过剩，可能导致空置率上升",
            "probability": 0.5,
            "impact": "medium",
            "mitigation": "深入调研市场供需，制定差异化定位策略"
        })
        
        # 融资风险
        if investment_amount > 50000:
            risks.append({
                "category": "融资风险",
                "level": "high",
                "description": "大额投资项目融资难度增加，利率波动影响成本",
                "probability": 0.3,
                "impact": "high",
                "mitigation": "多元化融资渠道，锁定利率风险"
            })
        else:
            risks.append({
                "category": "融资风险",
                "level": "low",
                "description": "投资规模适中，融资压力较小",
                "probability": 0.2,
                "impact": "low",
                "mitigation": "保持良好的银行授信"
            })
        
        # 运营风险
        risks.append({
            "category": "运营风险",
            "level": "low",
            "description": "项目运营管理能力对收益影响较大",
            "probability": 0.3,
            "impact": "medium",
            "mitigation": "组建专业运营团队或委托专业机构"
        })
        
        # 工期风险
        if timeline > 36:
            risks.append({
                "category": "工期风险",
                "level": "medium",
                "description": "项目周期较长，可能面临工期延误",
                "probability": 0.4,
                "impact": "medium",
                "mitigation": "制定详细计划，预留缓冲时间"
            })
        
        high_risks = [r for r in risks if r["level"] == "high"]
        medium_risks = [r for r in risks if r["level"] == "medium"]
        
        return {
            "city": city,
            "project_type": project_type,
            "total_risks": len(risks),
            "high_risk_count": len(high_risks),
            "medium_risk_count": len(medium_risks),
            "risks": risks,
            "risk_summary": f"共识别{len(risks)}个风险点，其中{len(high_risks)}个高风险，{len(medium_risks)}个中风险"
        }


class GenerateRiskReportInput(BaseModel):
    """风险报告生成输入参数"""
    project_name: str = Field(description="项目名称")
    city: str = Field(description="城市名称")
    risks: List[Dict] = Field(description="风险列表")


class GenerateRiskReportTool(BaseTool):
    name: str = "generate_risk_report"
    description: str = "生成完整的风险评估报告"
    args_schema: type = GenerateRiskReportInput
    
    def _run(self, project_name: str, city: str, risks: List[Dict]) -> Dict:
        """生成风险报告"""
        high_risks = [r for r in risks if r["level"] == "high"]
        medium_risks = [r for r in risks if r["level"] == "medium"]
        low_risks = [r for r in risks if r["level"] == "low"]
        
        overall_risk_score = sum({
            "high": 3,
            "medium": 2,
            "low": 1
        }[r["level"]] for r in risks) / len(risks) if risks else 0
        
        if overall_risk_score >= 2.5:
            risk_level = "高"
            color_code = "red"
        elif overall_risk_score >= 1.5:
            risk_level = "中"
            color_code = "yellow"
        else:
            risk_level = "低"
            color_code = "green"
        
        return {
            "project_name": project_name,
            "city": city,
            "report_date": "2024-01-15",
            "overall_risk_level": risk_level,
            "risk_score": round(overall_risk_score, 2),
            "risk_breakdown": {
                "high": len(high_risks),
                "medium": len(medium_risks),
                "low": len(low_risks)
            },
            "detailed_risks": risks,
            "recommendations": [
                "建立风险监测机制，定期评估风险变化",
                "针对高风险点制定专项应对预案",
                "保持充足的流动性储备应对突发风险",
                "与专业机构合作进行风险对冲"
            ],
            "summary": f"{project_name}（{city}）风险评估报告显示，项目整体风险等级为{risk_level}。"
                      f"建议重点关注{len(high_risks)}个高风险点，并制定相应的风险应对措施。"
        }


class GetComplianceSuggestionsInput(BaseModel):
    """合规建议输入参数"""
    city: str = Field(description="城市名称")
    project_type: str = Field(description="项目类型")
    issues: List[str] = Field(description="已识别的合规问题")


class GetComplianceSuggestionsTool(BaseTool):
    name: str = "get_compliance_suggestions"
    description: str = "针对合规问题提供优化建议"
    args_schema: type = GetComplianceSuggestionsInput
    
    def _run(self, city: str, project_type: str, issues: List[str]) -> Dict:
        """获取合规建议"""
        suggestions = []
        
        if "容积率" in " ".join(issues):
            suggestions.append({
                "issue": "容积率超标",
                "suggestion": "1. 申请调整规划指标；2. 增加配套设施换取容积率奖励；3. 分期开发降低单期规模",
                "priority": "high"
            })
        
        if "建筑面积" in " ".join(issues):
            suggestions.append({
                "issue": "建筑面积不足",
                "suggestion": "1. 扩大项目规模；2. 调整产品组合；3. 申请特殊政策豁免",
                "priority": "medium"
            })
        
        suggestions.append({
            "issue": "通用合规建议",
            "suggestion": "1. 提前与规划部门沟通；2. 聘请专业咨询机构；3. 预留合规调整时间",
            "priority": "medium"
        })
        
        return {
            "city": city,
            "project_type": project_type,
            "issues": issues,
            "suggestions": suggestions,
            "summary": f"针对识别到的{len(issues)}个合规问题，已提供{len(suggestions)}条优化建议"
        }


# 风险合规工具列表
RISK_TOOLS = [
    CheckPolicyComplianceTool(),
    IdentifyRiskPointsTool(),
    GenerateRiskReportTool(),
    GetComplianceSuggestionsTool()
]
