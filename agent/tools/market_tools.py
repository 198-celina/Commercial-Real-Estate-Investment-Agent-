from typing import Dict, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GetRealEstateMarketInput(BaseModel):
    """获取地产行情输入参数"""
    city: str = Field(description="城市名称，如：上海、北京")
    area: Optional[str] = Field(description="区域名称，如：陆家嘴、中关村")
    property_type: str = Field(description="物业类型，如：写字楼、商铺、公寓")


class GetRealEstateMarketTool(BaseTool):
    name: str = "get_real_estate_market"
    description: str = "获取商业地产市场行情数据，包括价格走势、租金水平、空置率等"
    args_schema: type = GetRealEstateMarketInput
    
    def _run(self, city: str, area: Optional[str] = None, property_type: str = "写字楼") -> Dict:
        """执行获取地产行情"""
        # 模拟返回市场行情数据
        return {
            "city": city,
            "area": area,
            "property_type": property_type,
            "avg_rent": {
                "office": {"monthly_per_sqm": 150, "trend": "stable"},
                "retail": {"monthly_per_sqm": 80, "trend": "down"},
                "apartment": {"monthly_per_sqm": 60, "trend": "up"}
            },
            "vacancy_rate": {
                "office": 0.12,
                "retail": 0.18,
                "apartment": 0.08
            },
            "price_per_sqm": {
                "office": 85000,
                "retail": 120000,
                "apartment": 65000
            },
            "market_summary": f"{city}{area or ''}商业地产市场整体平稳，写字楼租金保持稳定，零售物业空置率略有上升"
        }


class GetPolicyInfoInput(BaseModel):
    """获取政策信息输入参数"""
    city: str = Field(description="城市名称")
    policy_type: Optional[str] = Field(description="政策类型：土地政策、金融政策、限购政策等")


class GetPolicyInfoTool(BaseTool):
    name: str = "get_policy_info"
    description: str = "获取房地产相关政策信息，包括最新政策解读和影响分析"
    args_schema: type = GetPolicyInfoInput
    
    def _run(self, city: str, policy_type: Optional[str] = None) -> Dict:
        """执行获取政策信息"""
        return {
            "city": city,
            "policy_type": policy_type,
            "latest_policies": [
                {
                    "title": "关于促进商业地产健康发展的若干意见",
                    "date": "2024-01-15",
                    "content": "鼓励商业地产转型升级，支持存量资产盘活",
                    "impact": "积极",
                    "details": "对符合条件的商业地产项目给予税收优惠和融资支持"
                },
                {
                    "title": "城市更新实施细则",
                    "date": "2024-02-20",
                    "content": "推进中心城区老旧商业设施改造升级",
                    "impact": "积极",
                    "details": "提供容积率奖励和配套设施支持"
                }
            ],
            "policy_summary": f"{city}近期政策环境较为宽松，有利于商业地产投资"
        }


class GetLandInfoInput(BaseModel):
    """获取地块信息输入参数"""
    city: str = Field(description="城市名称")
    land_id: Optional[str] = Field(description="地块编号")
    location: Optional[str] = Field(description="地块位置")


class GetLandInfoTool(BaseTool):
    name: str = "get_land_info"
    description: str = "获取地块详细信息，包括位置、面积、规划用途、出让条件等"
    args_schema: type = GetLandInfoInput
    
    def _run(self, city: str, land_id: Optional[str] = None, location: Optional[str] = None) -> Dict:
        """执行获取地块信息"""
        return {
            "city": city,
            "land_id": land_id or "LD-2024-001",
            "location": location or "市中心商务区",
            "area": 12000,  # 平方米
            "land_use": "商业/办公",
            "floor_area_ratio": 5.0,
            "building_density": 0.4,
            "green_ratio": 0.25,
            "estimated_price": 15000,  # 元/平方米
            "development_period": 36,  # 个月
            "restrictions": ["自持比例不低于50%", "需配套建设公共服务设施"]
        }


class PredictMarketTrendInput(BaseModel):
    """市场趋势预测输入参数"""
    city: str = Field(description="城市名称")
    property_type: str = Field(description="物业类型")
    forecast_period: str = Field(description="预测周期：短期(6个月)、中期(1年)、长期(3年)")


class PredictMarketTrendTool(BaseTool):
    name: str = "predict_market_trend"
    description: str = "预测商业地产市场未来走势"
    args_schema: type = PredictMarketTrendInput
    
    def _run(self, city: str, property_type: str, forecast_period: str = "中期") -> Dict:
        """执行市场趋势预测"""
        trends = {
            "短期": {
                "office": {"price_trend": "stable", "rent_trend": "slight_up"},
                "retail": {"price_trend": "slight_down", "rent_trend": "down"},
                "apartment": {"price_trend": "up", "rent_trend": "up"}
            },
            "中期": {
                "office": {"price_trend": "up", "rent_trend": "stable"},
                "retail": {"price_trend": "stable", "rent_trend": "stable"},
                "apartment": {"price_trend": "up", "rent_trend": "up"}
            },
            "长期": {
                "office": {"price_trend": "up", "rent_trend": "up"},
                "retail": {"price_trend": "up", "rent_trend": "stable"},
                "apartment": {"price_trend": "up", "rent_trend": "up"}
            }
        }
        
        return {
            "city": city,
            "property_type": property_type,
            "forecast_period": forecast_period,
            "trend": trends.get(forecast_period, {}).get(property_type, {}),
            "confidence": 0.75,
            "recommendation": f"{city}{property_type}市场{forecast_period}展望：{trends.get(forecast_period, {}).get(property_type, {}).get('price_trend', 'stable')}"
        }


# 市场分析工具列表
MARKET_TOOLS = [
    GetRealEstateMarketTool(),
    GetPolicyInfoTool(),
    GetLandInfoTool(),
    PredictMarketTrendTool()
]
