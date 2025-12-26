# 🎓 AI 智能学习操作系统 (Intelligent Learning OS)

一个基于大语言模型的智能学习平台，采用"教学-评估-迁移测试-掌握"的闭环学习模式，确保学生真实掌握知识点。

## 📋 系统概述

### 核心特性
- **五大学科支持**：语文、数学、英语、历史、政治
- **AI 智能导师**：基于 LangChain 的对话式教学 Agent
- **三级评估系统**：A/B/C 三个理解等级，科学评估学习效果
- **迁移测试**：达到 A 级后触发应用题测试，验证举一反三能力
- **补救机制**：连续失败 3 次自动切换教学策略
- **多题型支持**：选择题、判断题、问答题、填空题、应用题

### 系统架构
```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit 前端                           │
│    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│    │   学生端     │ │   管理端     │ │   学科选择   │       │
│    └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI 后端                             │
│    ┌──────────────────────────────────────────────────┐     │
│    │              RESTful API 接口                     │     │
│    └──────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent 层                               │
│    ┌────────────┐ ┌────────────┐ ┌────────────┐            │
│    │LearningAgent│ │TeachingAgent│ │AssessmentAgent│         │
│    │ (核心调度)  │ │ (启发教学)  │ │ (深度评估)  │           │
│    └────────────┘ └────────────┘ └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangChain + LLM                             │
│         支持 OpenAI / 通义千问 / 智谱AI / DeepSeek 等        │
└─────────────────────────────────────────────────────────────┘
```

## 📁 文件结构

```
intelligent-learning-os/
├── config.py          # 配置文件（API密钥、服务器设置）
├── models.py          # Pydantic 数据模型定义
├── database.py        # 内存数据库 + 预置数据
├── agents.py          # LangChain AI Agent 实现
├── backend.py         # FastAPI 后端服务
├── frontend.py        # Streamlit 前端界面
├── requirements.txt   # Python 依赖包
└── README.md          # 项目文档
```

### 文件说明

| 文件 | 作用 |
|------|------|
| `config.py` | 配置 API 密钥、Base URL、模型名称等，**使用前必须修改** |
| `models.py` | 定义所有数据结构：Question、KnowledgeItem、Session 等 |
| `database.py` | 内存数据库实现，包含 5 个学科的预置知识点和题目 |
| `agents.py` | 三个核心 Agent：LearningAgent(调度)、TeachingAgent(教学)、AssessmentAgent(评估) |
| `backend.py` | FastAPI 服务器，提供 RESTful API 接口 |
| `frontend.py` | Streamlit 界面，包含学生端和管理端两种模式 |

## 🚀 快速开始

### 1. 环境要求
- Python 3.9+
- pip 包管理器

### 2. 安装依赖

```bash
# 克隆或下载项目后进入目录
cd intelligent-learning-os

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置 API 密钥

编辑 `config.py` 文件，填入你的 LLM API 信息：

```python
# OpenAI 配置示例
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
API_BASE_URL = "https://api.openai.com/v1"
MODEL_NAME = "gpt-3.5-turbo"

# 通义千问配置示例
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
API_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-turbo"

# 智谱AI配置示例
API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxx"
API_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
MODEL_NAME = "glm-4-flash"

# DeepSeek配置示例
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
API_BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"
```

### 4. 启动系统

**需要开启两个终端窗口：**

**终端 1 - 启动后端服务：**
```bash
python backend.py
```
看到以下信息表示后端启动成功：
```
╔══════════════════════════════════════════════════════════════╗
║           🎓 AI 智能学习操作系统                              ║
║                     v1.0.0                                   ║
║   后端服务启动中...                                          ║
║   API 文档: http://127.0.0.1:8000/docs                       ║
╚══════════════════════════════════════════════════════════════╝
```

**终端 2 - 启动前端服务：**
```bash
streamlit run frontend.py
```
看到以下信息表示前端启动成功：
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

### 5. 访问系统

打开浏览器访问：**http://localhost:8501**

- API 文档：http://localhost:8000/docs

## 📱 功能说明

### 学生端功能

#### 1. 学科选择
- 进入系统后，选择想要学习的科目
- 支持：语文、数学、英语、历史、政治

#### 2. AI 导师对话
- 与 AI 导师进行自然语言对话
- AI 会根据学科加载对应知识点
- 采用苏格拉底式提问引导学习

#### 3. 评估系统
- 输入"练习"、"做题"等触发练习模式
- 系统自动出题并评估回答
- 评估等级：
  - **A级**：完全理解，触发迁移测试
  - **B级**：基本理解，需要更多练习
  - **C级**：理解不足，需要重新学习

#### 4. 迁移测试
- A级后自动触发应用题测试
- 验证学生能否举一反三
- 通过后标记知识点为"已掌握"

#### 5. 补救机制
- 连续失败3次触发补救教学
- AI 自动切换教学策略
- 用更简单的方式重新讲解

### 管理端功能

#### 1. 数据看板
- 活跃学生数
- 知识库条目数
- AI 交互次数
- 全站平均掌握度

#### 2. 题目管理
- 按学科、题型、难度筛选
- 支持增删改查 (CRUD)
- 多种题型支持

#### 3. 知识库管理
- 上传文本/PDF/链接形式的知识点
- 关联学科和标签
- 设置要点和常见误区

#### 4. 系统日志
- 实时查看系统动态
- 记录知识库更新、系统操作等

## 📊 预置数据

系统预置了每个学科的知识点和题目：

| 学科 | 知识点 | 题目数 | 主题示例 |
|------|--------|--------|----------|
| 语文 | 2 | 4 | 修辞手法、古诗鉴赏 |
| 数学 | 2 | 4 | 一元二次方程、函数基础 |
| 英语 | 2 | 4 | 时态、被动语态 |
| 历史 | 2 | 4 | 改革开放、秦朝统一 |
| 政治 | 2 | 4 | 市场经济、公民权利 |

## 🔧 API 接口

主要接口列表：

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/sessions | 创建学习会话 |
| POST | /api/chat | 发送消息获取 AI 回复 |
| GET | /api/questions | 获取题目列表 |
| POST | /api/questions | 创建题目 |
| GET | /api/knowledge | 获取知识点列表 |
| POST | /api/knowledge | 创建知识点 |
| GET | /api/admin/stats | 获取统计数据 |

完整 API 文档访问：http://localhost:8000/docs

## ⚠️ 注意事项

1. **必须先启动后端**：前端依赖后端 API，请确保后端先启动
2. **配置 API 密钥**：使用前必须在 `config.py` 中配置有效的 LLM API
3. **内存数据库**：当前使用内存存储，重启后数据会重置
4. **网络连接**：需要访问 LLM API，确保网络通畅

## 🔄 扩展开发

### 添加持久化存储
可以将 `database.py` 中的内存存储替换为：
- SQLite / PostgreSQL
- MongoDB
- Redis

### 添加用户认证
可以在 FastAPI 中添加：
- JWT Token 认证
- OAuth2 登录

### 添加更多 Agent
可以在 `agents.py` 中扩展：
- 总结 Agent
- 练习生成 Agent
- 学情分析 Agent

## 📝 常见问题

**Q: 启动报错 "API 请求失败"**
A: 检查后端是否正常运行，确认 config.py 中的 BACKEND_URL 配置正确

**Q: AI 回复 "服务暂时不可用"**
A: 检查 API_KEY 是否正确配置，网络是否能访问 LLM 服务

**Q: 如何切换不同的 LLM**
A: 修改 config.py 中的 API_KEY、API_BASE_URL 和 MODEL_NAME

## 📄 License

MIT License

---

🎓 **AI 智能学习操作系统** - 让学习更智能，让成长更高效！
