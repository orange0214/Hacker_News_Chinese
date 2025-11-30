from token import OP
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import html
from typing import Optional, List

class HNStoryRaw(BaseModel):
    """
    This Pydantic model is responsible for:
    - Receiving the response from the HN API
    - Performing field cleaning/normalization so downstream usage is consistent
    """
    hn_id: int = Field(alias="id")
    original_title: str = Field(alias="title")
    original_url: Optional[str] = Field(default=None, alias="url")
    score: int = 0
    by: str
    posted_at: datetime = Field(default_factory=datetime.now, alias="time")
    type: str
    
    hn_text_content: Optional[str] = Field(default=None, alias="text")

    @field_validator("hn_text_content", mode="before")
    @classmethod
    def unescape_html(cls, v):
        return html.unescape(v or "")
    
    @field_validator('posted_at', mode='before')
    @classmethod
    def timestamp_to_datetime(cls, v):
        if v:
            return datetime.fromtimestamp(v)
        return datetime.now()

class AITranslatedResult(BaseModel):
    # LLM translated and summarized result
    topic: str = Field(description="文章领域标签")
    title_cn: str = Field(description="中文标题")
    summary: str = Field(description="深度摘要")
    key_points: List[str] = Field(description="关键要点", min_items=3, max_items=5)
    tech_stack: List[str] = Field(default_factory=list, description="技术栈")
    takeaway: str = Field(description="独立洞察")
    score: int = Field(description="评分", ge=0, le=100)
    source_trans: str = Field(description="全文精译")

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

class Article(BaseModel):
    """
    This Pydantic model represents an enriched HN article, containing:
    1. Basic information returned by the HN API (hn_id, original_title, original_url, score, etc.)
    2. The main article body/content extracted by the crawler (raw_content)
    3. AI-generated results, such as summary, translated_title, detailed_analysis, etc.
    """
    hn_id: int
    original_title: str
    original_url: Optional[str]
    score: int
    posted_at: datetime

    raw_content: str

    translated_title: Optional[str] = None
    summary: Optional[str] = None
    detailed_analysis: Optional[AITranslatedResult] = None
    
    class Config:
        # allow reading data from ORM objects (if we use SQLAlchemy in the future)
        from_attributes = True 
        # when saving to the database, let Pydantic automatically convert detailed_analysis to JSON
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
