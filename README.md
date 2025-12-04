# Hacker News Chinese

**Hacker News Chinese** 是一个 AI 驱动的技术资讯聚合平台。旨在打破语言障碍，通过自动化流程获取 Hacker News 热门文章，利用大语言模型（LLM）进行中文翻译与深度总结，帮助用户高效获取高质量技术资讯。

## 核心功能

- **自动聚合**: 定时抓取 Hacker News 的 Top Stories。
- **智能解析**: 
    - 使用 Jina Reader 提取网页核心内容。
    - 完整保留 Hacker News 原贴的文本描述 (Text)，对于 Show HN / Ask HN 至关重要。
- **AI 总结**: 
    - 综合原文标题、原贴描述和网页正文进行分析。
    - 生成中文标题、深度总结以及原文翻译。
- **数据持久化**: 结构化存储文章元数据及分析结果至 Supabase。
- **RAG 问答** (开发中): 支持基于文章内容的 AI 问答交互。

## 技术栈

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL + pgvector)
- **AI Services**:
  - LLM: Gemini (via OpenAI SDK) for summarization
  - Content Extraction: Jina Reader API
- **Package Management**: uv
- **Observability**: Loguru (AOP-based logging)

## 快速开始

### 1. 环境准备

- Python 3.12
- uv

### 2. 安装依赖

```bash
git clone <repository-url>
cd Hacker_News_Chinese
uv sync
```

### 3. 配置环境变量

复制 `.env.example` (如果存在) 或新建 `.env` 文件，填入以下配置：

```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# AI Services
OPENAI_API_KEY=your_openai_api_key
JINA_API_KEY=your_jina_api_key

# App
LOG_LEVEL=INFO
```

### 4. 运行服务

```bash
# 开发模式
uv run uvicorn app.main:app --reload
# 或者
uv run dev

# 或使用 Makefile (如有)
make run
```

API 文档地址: `http://localhost:8000/api/docs`

## 项目结构

```
app/
├── api/            # API 路由与依赖
├── core/           # 核心配置 (Config, Prompts)
├── db/             # 数据库连接 (Supabase)
├── models/         # Pydantic 数据模型
├── repositories/   # 数据访问层
├── services/       # 业务逻辑 (HN Fetcher, Extraction, AI Summary)
└── main.py         # 应用入口
```

## 开发状态

当前处于 MVP 开发阶段。详细规划请参考 [PRD.md](./PRD.md) 和 [TODO.md](./TODO.md)。
