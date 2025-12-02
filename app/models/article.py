from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Article(BaseModel):
    """
    This Pydantic model represents an enriched HN article, containing:
    1. Basic information returned by the HN API (hn_id, original_title, original_url, score, etc.)
    2. The main article body/content extracted by the crawler (raw_content)
    3. AI-generated results, such as summary, translated_title, detailed_analysis, etc.
    """
    hn_id: int
    type: str
    by: Optional[str] = Field(default=None, description="The username of the item's author")
    posted_at: datetime
    
    original_title: str
    original_url: Optional[str]
    original_text: Optional[str]
    score: int

    kids: Optional[List[int]]
    parent: Optional[int]
    poll: Optional[int]
    parts: Optional[List[int]]
    descendants: Optional[int]

    deleted: Optional[bool]
    dead: Optional[bool]

    raw_content: str
    image_urls: Optional[List[str]]

    detailed_analysis: Optional[AITranslatedResult]
    comment_analysis: Optional[List[CommentAnalysis]]
    
    class Config:
        # allow reading data from ORM objects (if we use SQLAlchemy in the future)
        from_attributes = True 
        # when saving to the database, let Pydantic automatically convert detailed_analysis to JSON
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AITranslatedResult(BaseModel):
    # LLM translated and summarized result
    topic: str = Field(description="Article topic label")
    title_cn: str = Field(description="Chinese title")
    summary: str = Field(description="In-depth summary")
    key_points: List[str] = Field(description="Key points", min_items=3, max_items=5)
    tech_stack: List[str] = Field(default_factory=list, description="Tech stack")
    takeaway: str = Field(description="Independent insight")
    score: int = Field(description="Score", ge=0, le=100)
    source_trans: str = Field(description="Full-text translation")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Mental Model",
                "title_cn": "单点收敛：高压搜索中的概率最优解",
                "summary": "作者回顾了十多年前两次申请研究生失败的经历...",
                "key_points": [
                    "将连续失败重构为概率搜索",
                    "成功阈值的非对称性"
                ],
                "tech_stack": [],
                "takeaway": "文章基于个人叙事，缺乏实证数据支撑...",
                "score": 20,
                "source_trans": "正文翻译内容..."
            }
        }

class CommentAnalysis(BaseModel):
    comment_trans: str = Field(description="Full-text translation of the comment")