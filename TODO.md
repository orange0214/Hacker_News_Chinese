#### 11/25/2025
- 项目架构初步搭建
- 整合supabase
- 注册、登录、鉴权功能完成

#### 11/26/2025
- 主要功能初步设计
  - Hacker News story schema
  - 查询 -> 提取网页关键内容（jina） -> AI 翻译，总结流程设计
  - PRD.md
- Hacker News 异步访问API获取best, top, new stories 逻辑完成

#### 11/27/2025
- 将表结构存入supabase
  - 根据 hn_id 查询article存在
  - 添加article进入db

#### 11/28/2025
- 并行从Jina获得markdown形式的网页信息
- 并行将md格式的信息发送给API

#### 11/29/2025
- hn service 中print输出统一化 [HN] -> [HNService]
- 参考Jina官方文档通过``"X-Retain-Images": "none"`` 关闭图片转化
- 更新prompt
- 在schemas/hn.py中实现AITranslatedResult类
  
#### 11/30/2025
- 发现问题：AI分析结果中没有加入title与作者写的内容

#### 12/01/2025
- 修改 `HNRaw` 类，补充 `kids`, `descendants` 等官方 API 返回的字段。
- 修改 `Articel`类，让其符合更改的 `HNRaw`类
- 修改 `schema.sql` 表
- 实现  `news_ingestor.py` (未测试)
- 参考DDD进行部分重构：将Article等class移动至models/
- 解决问题：AI分析结果中没有加入title与作者写的内容-更新prompt与更改相关业务逻辑代码

#### 12/02/2025
- 迁移poetry至uv

#### 12/03/2025
- 测试 `news_ingestor.py` 并实现 Swagger 触发接口 (`POST /api/news/ingest`)
- BugFix: 从 Poetry 迁移至 uv 后，默认安装的最新版 `httpx` (0.28.1) / `httpcore` (1.0.9) 导致在 Windows 环境下连接 DeepSeek API 频繁出现 `RemoteProtocolError` (Peer closed connection)。
  - 尝试方案：降级 HTTP/1.1、禁用连接池 (Keep-Alive=0) 均未能根治（DeepSeek 服务端对连接关闭处理较激进）。
  - 最终方案：切换 LLM Provider 至 **Gemini** (配合 OpenAI SDK)，连接稳定，数据摄入流程跑通。
- logger.py 初始化
  - 尚未完成AOP decorators
  - 尚未修改服务将logger与AOP引入
  
#### 12/04/2025
- 完成AOP修饰器并在3个services以及pipeline中调用，定义error.log与news_ingestor.log
- 引入 **APScheduler** (`AsyncIOScheduler`) 完成定时任务调度功能

#### 12/05/2025
- supabase中清理rows(ai分析的score改为ai_score),并测试ingestor功能
- debug in ingestor pipeline
- 重构DDD
  - 移动 `app/schemas/contexts.py` -> `app/services/contexts/story_contexts.py` (Pipeline 上下文)
  - 保留 `HNRaw` 在 `app/schemas/external/hn.py` (外部 DTO)
- 构造 schemas/article.py (只定义了request model)


TODO:
- Articles 接口规划
  - [ ] API 定义: `GET /api/articles`
  - [ ] 请求参数 (Query Params):
    - `page`: 页码 (int, default: 1)
    - `size`: 每页数量 (int, default: 20)
    - `sort_by`: 排序字段 (enum: `posted_at`, `score`, `ai_score`, default: `posted_at`)
      - `score`: Hacker News 原始热度
      - `ai_score`: AI 内容质量评分
    - `order`: 排序方向 (enum: `desc`, `asc`, default: `desc`)
  - [ ] 响应结构 (Response):
    - `items`: 文章列表 (List[ArticleSchema])
      - 基础信息:
        - `id`: 数据库 ID (int)
        - `hn_id`: Hacker News ID (int)
        - `original_title`: 原文标题 (str)
        - `original_url`: 原文链接 (str)
        - `posted_at`: 发布时间 (datetime)
        - `score`: HN 分数 (int)
        - `by`: 作者 (str)
        - `type`: 文章类型 (str)
      - AI 分析内容 (detailed_analysis):
        - `title_cn`: 中文标题 (str)
        - `summary`: 深度摘要 (str)
        - `topic`: 文章主题/领域 (str)
        - `key_points`: 关键点列表 (List[str])
        - `tech_stack`: 涉及技术栈 (List[str])
        - `takeaway`: 核心洞察/Takeaway (str)
        - `ai_score`: AI 评分 (int)
      - 统计信息:
        - `descendants`: 评论数 (int)
      - 状态:
        - `deleted`: 是否已删除 (bool)
        - `dead`: 是否已失效 (bool)
    - `total`: 总记录数 (int)
    - `page`: 当前页码 (int)
    - `size`: 当前每页数量 (int)
    - `total_pages`: 总页数 (int)
  - [ ] 业务逻辑:
    - 校验参数
    - 构建 Supabase 查询 (分页 + 排序)
    - 转换数据模型为 Pydantic Schema
    - 错误处理 (500, etc.)


- 研究AI翻译总结的高性能prompt（prompt training）
- RAG
- （Post-MVP）：集成多模态视觉模型（Vision Model），对文章中的关键图片进行语义描述提取，并作为上下文输入给 LLM 以生成更完整的总结。