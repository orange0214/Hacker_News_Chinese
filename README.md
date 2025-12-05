# Hacker News Chinese

**Hacker News Chinese** 是一个 AI 驱动的技术资讯聚合平台，旨在打破语言障碍，通过自动化流程获取 Hacker News 热门文章，并利用大语言模型（LLM）生成中文摘要与翻译，帮助用户高效获取高质量技术资讯。

## 核心功能

- **自动聚合**: 定时抓取 Hacker News Top Stories。
- **智能解析**: 
    - 使用 Jina Reader 提取网页核心内容。
    - 完整保留 Hacker News 原贴的文本描述 (Text)。
- **AI 总结**: 
    - 综合原文标题、原贴描述和网页正文进行分析。
    - 生成中文标题、深度总结及原文翻译。
- **数据持久化**: 结构化存储文章元数据及分析结果至 Supabase。

## 技术栈

- **Backend**: FastAPI (Python 3.12+)
- **Database**: Supabase (PostgreSQL + pgvector)
- **AI Services**: Gemini (Summarization), Jina Reader (Extraction)
- **Tooling**: uv (Package Management), Loguru (Logging), APScheduler (Task Scheduling)

## 快速开始

### 1. 环境准备
- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

### 2. 安装依赖

```bash
git clone <repository-url>
cd Hacker_News_Chinese
uv sync
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：


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
├── api/            # API 路由 (Endpoints, Dependencies)
├── core/           # 核心组件 (Config, Logger, Ingestor, Scheduler)
├── db/             # 数据库连接 (Supabase)
├── models/         # Pydantic 数据模型
├── repositories/   # 数据访问层
├── schemas/        # 数据传输对象 (DTOs)
├── services/       # 业务逻辑 (HN Fetcher, Extraction, AI Summary)
└── main.py         # 应用入口
```

## 开发状态

当前处于 MVP 开发阶段。详细规划请参考 [PRD.md](./PRD.md) 和 [TODO.md](./TODO.md)。
