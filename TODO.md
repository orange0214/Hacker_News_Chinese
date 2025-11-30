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


TODO:
- 跑通pipeline，core/news_ingestor.py
- 迁移poetry至uv
- 每12小时执行一次轮询获取内容
- 研究AI翻译总结的高性能prompt
- 将AI生成内容并入CreateArticle类存入数据库
- 构建日志系统(不同的模块构造不同的日志，例如fetching from HN 存入hn_fetching.log?)
- （Post-MVP）：集成多模态视觉模型（Vision Model），对文章中的关键图片进行语义描述提取，并作为上下文输入给 LLM 以生成更完整的总结。


# Hacker News Chinese Implementation Plan

## 1. Database & Repository Layer (Priority High)

- [x] **Schema Setup**: Create `articles` table in Supabase matching PRD Section 4.
- [x] **Repository Implementation**: Create `app/repositories/article_repository.py`.
    - `exists(hn_id: int) -> bool`: Check if article already exists (Deduplication).
    - `create(article: Article) -> Article`: Save processed article to DB.

## 2. Content Extraction & AI Services (Priority High)

- [x] **Dependencies**: Add `openai` (or preferred LLM lib) and `requests`/`httpx` to `pyproject.toml`.
- [x] **Config**: Update `app/core/config.py` to include `JINA_API_KEY` and `OPENAI_API_KEY`.
- [ ] **Content Service**: Create `app/services/content_extractor.py` using Jina Reader API.
- [ ] **AI Service**: Create `app/services/ai_service.py`.
    - Implement translation prompt.
    - Implement summarization/analysis prompt (JSON output).

## 3. Pipeline Integration (Priority Medium)

- [ ] **Update HNService**:
    - Integrate `ArticleRepository` to filter out existing stories.
    - Integrate `ContentService` to fetch body text.
    - Integrate `AIService` to process content.
    - Save final result to DB.

## 4. Scheduling (Priority Medium)

- [ ] **Scheduler**: Implement a background task (using `apscheduler` or `asyncio` loop) in `main.py` to run the fetch pipeline every 30 minutes.

## 5. Future Roadmap (Post-MVP)

- [ ] **Multimodal Analysis**: Implement an image processing pipeline using a Vision Model (e.g., Gemini Flash/GPT-4o) to caption key images and feed them into the summarization context.