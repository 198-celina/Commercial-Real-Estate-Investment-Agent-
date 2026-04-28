# 商业地产投资分析系统 - 项目总览

> 基于 Multi-Agent 架构的智能投资分析平台

---

## 📋 目录

1. [系统概述](#系统概述)
2. [系统架构](#系统架构)
3. [功能演示](#功能演示)
4. [API 接口文档](#api-接口文档)
5. [测试记录](#测试记录)
6. [项目文件说明](#项目文件说明)

---

## 系统概述

本系统采用 **主 Agent + 3个垂类 Agent** 的架构，专为商业地产投资分析设计。

### 技术栈
- **后端框架**：FastAPI (Python)
- **Agent 框架**：LangChain + LangGraph
- **向量数据库**：Milvus 2.3.5
- **会话存储**：Redis 4.6.0
- **LLM 服务**：通义千问 (qwen3.5-plus)

### 核心功能
| 功能 | 状态 | 说明 |
|------|------|------|
| 市场分析 | ✅ | 获取地产行情、政策解读、地块信息 |
| 收益测算 | ✅ | 计算租金收益、回报周期、IRR/NPV |
| 风险合规 | ✅ | 政策合规检查、风险识别、合规建议 |
| 智能对话 | ✅ | 基于 RAG 知识库的智能问答 |

---

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                  用户层                          │
│          企业微信 / OA / H5 / Web                │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│                 网关层                           │
│        Nginx 负载均衡 + Sentinel 限流            │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│                应用层                            │
│           FastAPI 服务网关                       │
│        ┌─────────────┐                          │
│        │  主 Agent    │ ← 意图识别、任务分发     │
│        └──────┬──────┘                          │
│               ↓                                 │
│    ┌──────────┼──────────┐                     │
│    ↓          ↓          ↓                     │
│  市场分析   收益测算   风险合规                 │
│  Agent      Agent      Agent                    │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│              数据服务层                          │
│   工具调用 │ RAG检索 │ LLM推理                  │
└─────────────────────────────────────────────────┘
```

### Agent 架构详情

| Agent | 职责 | 工具数量 |
|-------|------|---------|
| 主 Agent | 意图识别、任务路由、结果整合 | - |
| 市场分析 Agent | 行情查询、政策解读、趋势预测 | 4 |
| 收益测算 Agent | 租金计算、回报周期、IRR/NPV | 4 |
| 风险合规 Agent | 合规检查、风险识别、报告生成 | 4 |

---

## 功能演示

### 1. 市场分析示例

**输入**：分析上海陆家嘴商业地产投资价值

**输出**：
```json
{
  "city": "上海",
  "area": "陆家嘴",
  "result": {
    "success": true,
    "agent": "市场分析Agent",
    "result": [
      {
        "tool": "get_real_estate_market",
        "result": {
          "city": "上海",
          "property_type": "写字楼",
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
          "market_summary": "上海商业地产市场整体平稳，写字楼租金保持稳定，零售物业空置率略有上升"
        }
      }
    ]
  }
}
```

### 2. 收益测算示例

**输入**：建筑面积5000㎡，平均租金150元，总投资10000万

**输出**：
```json
{
  "project_name": "测试项目",
  "city": "上海",
  "total_investment": 10000,
  "area": 5000,
  "key_metrics": {
    "annual_gross_income": 810.0,
    "annual_operating_expenses": 300.0,
    "annual_net_income": 510.0,
    "cap_rate": 5.1,
    "payback_period": 19.6
  },
  "evaluation": {
    "grade": "C",
    "status": "一般",
    "summary": "测试项目位于上海，总投资10000万元，建筑面积5000平方米。预期年净收益510.0万元，资本化率5.1%，投资回报周期约19.6年。综合评估：一般(C级)"
  }
}
```

### 3. 风险合规示例

**输入**：上海写字楼项目，用地5000㎡，建筑20000㎡

**输出**：
```json
{
  "city": "上海",
  "project_type": "写字楼",
  "compliance_checks": [
    {
      "item": "容积率",
      "status": "pass",
      "message": "容积率4.00符合要求"
    },
    {
      "item": "最小建筑面积",
      "status": "pass",
      "message": "建筑面积符合要求"
    },
    {
      "item": "土地用途",
      "status": "pass",
      "message": "写字楼项目用地性质符合规划"
    },
    {
      "item": "配套设施",
      "status": "pass",
      "message": "配套设施比例符合当地规定"
    }
  ],
  "overall_status": "compliant",
  "summary": "上海写字楼项目政策合规检查通过"
}
```

---

## API 接口文档

### 接口列表

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/health/` | GET | 健康检查 |
| `/api/v1/chat/` | POST | 智能对话 |
| `/api/v1/investment/market/{city}` | GET | 市场分析 |
| `/api/v1/investment/revenue/calculate` | GET | 收益测算 |
| `/api/v1/investment/risk/{city}` | GET | 风险合规 |

### 接口详情

#### 1. 健康检查

**请求**：
```
GET /api/v1/health/
```

**响应**：
```json
{
  "status": "healthy",
  "service": "Multi-Agent Commercial Real Estate Investment Analysis System",
  "version": "1.0.0",
  "timestamp": "2026-04-28T15:57:06.265240"
}
```

#### 2. 智能对话

**请求**：
```
POST /api/v1/chat/
Content-Type: application/json

{
  "session_id": null,
  "message": "分析上海陆家嘴商业地产投资价值"
}
```

**响应**：
```json
{
  "session_id": "426a4a26-6ed9-4a50-bce4-6283624b64a5",
  "message": "市场分析已完成；收益测算已完成；风险合规审查已完成",
  "success": true,
  "analysis_type": "market_analysis",
  "metadata": {
    "intents": [
      "market_analysis",
      "revenue_calculation",
      "risk_compliance"
    ]
  }
}
```

#### 3. 市场分析

**请求**：
```
GET /api/v1/investment/market/上海?area=陆家嘴
```

**响应**：
```json
{
  "city": "上海",
  "area": "陆家嘴",
  "result": {
    "success": true,
    "agent": "市场分析Agent",
    "result": [
      {
        "tool": "get_real_estate_market",
        "result": {
          "city": "上海",
          "property_type": "写字楼",
          "avg_rent": {
            "office": {"monthly_per_sqm": 150, "trend": "stable"}
          },
          "vacancy_rate": {"office": 0.12},
          "price_per_sqm": {"office": 85000}
        }
      }
    ]
  }
}
```

#### 4. 收益测算

**请求**：
```
GET /api/v1/investment/revenue/calculate?area=5000&avg_rent=150&investment=10000
```

**响应**：
```json
{
  "project_name": "测试项目",
  "city": "上海",
  "total_investment": 10000,
  "area": 5000,
  "key_metrics": {
    "annual_gross_income": 810.0,
    "annual_net_income": 510.0,
    "cap_rate": 5.1,
    "payback_period": 19.6
  }
}
```

#### 5. 风险合规

**请求**：
```
GET /api/v1/investment/risk/上海?property_type=写字楼
```

**响应**：
```json
{
  "city": "上海",
  "project_type": "写字楼",
  "compliance_checks": [...],
  "overall_status": "compliant"
}
```

### 访问地址

- **API 文档 (Swagger)**：http://localhost:8000/docs
- **API 文档 (ReDoc)**：http://localhost:8000/redoc
- **测试页面**：test_demo.html

---

## 测试记录

### 测试环境

| 项目 | 值 |
|------|-----|
| 操作系统 | macOS |
| Python 版本 | 3.13.3 |
| 测试日期 | 2026-04-28 |

### 测试结果汇总

| 测试项 | 状态 | 说明 |
|--------|------|------|
| 依赖安装 | ✅ | 核心依赖全部安装成功 |
| 模块导入 | ✅ | FastAPI、Pydantic、LangChain、Agent |
| Redis 服务 | ✅ | Docker 容器运行，版本 4.6.0 |
| Milvus 服务 | ✅ | Milvus 2.3.5 default_server |
| API 服务 | ✅ | 端口 8000 正常运行 |
| 健康检查 | ✅ | 返回服务状态正常 |
| 对话接口 | ✅ | 会话创建成功，返回完整分析结果 |
| 市场分析 | ✅ | 返回租金、空置率、价格走势等数据 |
| 收益测算 | ✅ | 返回收益计算结果 |
| 风险合规 | ✅ | 返回风险分析结果 |
| RAG 知识库 | ✅ | 8 个文档已导入 |

### 遇到的问题及解决方案

| 问题 | 解决方案 |
|------|---------|
| Python 3.13 不兼容 pkg_resources | 降级 setuptools 到 69.5.1 |
| langchain API 版本不兼容 | 更新导入路径 (langchain_openai, langchain_core) |
| Pydantic v2 类型注解要求 | 添加 name/description/args_schema 类型注解 |
| initialize_agent 已移除 | 改用直接工具调用 |
| Redis 7.4.0 不兼容 | 降级到 4.6.0 |
| Milvus Lite 包不可用 | 改用 Milvus 2.3.5 default_server |

### RAG 知识库文档

| 序号 | 文档标题 | 类别 | 来源 |
|------|---------|------|------|
| 1 | 上海市商业地产市场分析报告（2024年Q1） | market_report | 上海市房地产交易中心 |
| 2 | 关于促进商业地产健康发展的若干意见 | policy | 上海市住建委 |
| 3 | 绿城·潮鸣东方项目介绍 | project_info | 绿城中国 |
| 4 | 黄浦区潮鸣街道地块出让信息 | land_info | 上海市规划和自然资源局 |
| 5 | 上海市城市更新实施细则 | policy | 上海市城市更新局 |
| 6 | 2024年上海商业地产投资趋势分析 | market_report | 戴德梁行研究部 |
| 7 | 绿城·潮鸣东方项目可行性研究报告 | feasibility_study | 绿城中国战略发展部 |
| 8 | 上海市黄浦区商业网点布局规划（2024-2035） | policy | 黄浦区商务委员会 |

---

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | FastAPI 主应用入口 |
| `test_demo.html` | 交互式测试页面（需要启动 API） |
| `demo.html` | 静态演示页面（可直接打开） |
| `ARCHITECTURE.md` | 系统架构设计文档 |
| `INTERVIEW_GUIDE.md` | 面试问题指南 |
| `CODE_INTERVIEW.md` | 代码面试题 |
| `TEST_LOG.md` | 测试记录文档 |
| `PROJECT_OVERVIEW.md` | 项目总览（本文件） |
| `data/sample_documents.json` | RAG 知识库文档 |
| `scripts/import_documents.py` | 文档导入脚本 |

---

## 启动方式

### 完整启动

```bash
# 1. 启动 Redis
docker run -d --name redis -p 6379:6379 redis:7-alpine

# 2. 启动 API 服务
source venv/bin/activate
OPENAI_API_KEY="sk-sp-d77b35030e6e46e6bdc440b3107bd0b8" \
OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1" \
uvicorn main:app --host 0.0.0.0 --port 8000

# 3. 访问
# API 文档: http://localhost:8000/docs
# 测试页面: open test_demo.html
```

### 仅测试（无需 API Key）

```bash
# 启动 API 服务（使用模拟数据）
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# 访问测试页面
open test_demo.html
```

---

*文档生成时间：2026-04-28*
*系统版本：v1.0.0*
