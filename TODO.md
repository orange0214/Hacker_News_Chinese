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
- 

TODO:
- 跑通pipeline，core/news_ingestor.py
- 迁移poetry至uv
- 每12小时执行一次轮询获取内容
- 研究AI翻译总结的高性能prompt
- 将AI生成内容并入CreateArticle类存入数据库
- 构建日志系统(不同的模块构造不同的日志，例如fetching from HN 存入hn_fetching.log?)
- （Post-MVP）：集成多模态视觉模型（Vision Model），对文章中的关键图片进行语义描述提取，并作为上下文输入给 LLM 以生成更完整的总结。



**中文简述:**
1. **AI 提示词优化**: 更新 System Prompt，使其能处理这种混合输入，并同时关注原贴描述和网页正文。
2. 修改 translate_service.py
3. **数据整合逻辑**: 调整 `NewsIngestor`，在发送给 AI 之前，将 HN 原贴的 `title`、`text` (如有) 和 Jina 抓取的网页正文合并。

---

### Detailed Tasks

#### 1. Schema Update (`app/schemas/hn.py`)
- [ ] Update `HNRaw` class to include all fields from the official HN API:
    - `kids`: `List[int]` (optional)
    - `descendants`: `int` (optional)
    - `parts`: `List[int]` (optional)
    - `poll`: `int` (optional)
    - `deleted`: `bool` (optional)
    - `dead`: `bool` (optional)
    - `parent`: `int` (optional)

#### 2. Pipeline / Ingestor Update (`app/core/news_ingestor.py`)
- [ ] Modify `run` method to construct a composite input for the AI Service.
    - **Logic**:
        ```python
        combined_text = f"""
        Title: {story.title}
        Original Text: {story.text or "N/A"}
        ---
        Scraped Content:
        {extracted_content}
        """
        ```
    - Ensure "Ask HN" stories (no URL) are handled correctly by passing `story.text` as the primary content.

#### 3. AI Service Refactor (`app/services/translate_service.py` & `prompts.py`)
- [ ] Update `Prompts.SUMMARIZE_SYSTEM` to instruct the LLM to:
    - Consider both the user's original description (often contains key context for "Show HN") and the linked article content.
    - Handle cases where one source might be empty.

#### 4. Documentation
- [ ] Verify `PRD.md` and `README.md` reflect this "Hybrid Input" strategy.
