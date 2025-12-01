from token import OP
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import html
from typing import Optional, List

class HNRaw(BaseModel):
    """
    This Pydantic model is responsible for:
    - Receiving the response from the HN API
    - Performing field cleaning/normalization so downstream usage is consistent
    - Strictly matching the official HN API specification
    """
    # Required fields
    hn_id: int = Field(alias="id", description="The item's unique id")
    type: str = Field(description="Type of item: job, story, comment, poll, or pollopt")
    by: Optional[str] = Field(default=None, description="The username of the item's author")
    posted_at: datetime = Field(default_factory=datetime.now, alias="time", description="Creation date in Unix Time")
    
    # Optional fields (based on type and state)
    original_title: Optional[str] = Field(default=None, alias="title", description="The title of the story, poll or job. HTML.")
    original_url: Optional[str] = Field(default=None, alias="url", description="The URL of the story")
    hn_text_content: Optional[str] = Field(default=None, alias="text", description="The comment, story or poll text. HTML.")
    score: Optional[int] = Field(default=0, description="The story's score, or the votes for a pollopt")
    
    # Relationship fields
    kids: Optional[List[int]] = Field(default=None, description="The ids of the item's comments")
    parent: Optional[int] = Field(default=None, description="The comment's parent: either another comment or the relevant story")
    poll: Optional[int] = Field(default=None, description="The pollopt's associated poll")
    parts: Optional[List[int]] = Field(default=None, description="A list of related pollopts")
    descendants: Optional[int] = Field(default=None, description="In the case of stories or polls, the total comment count")
    
    # Status fields
    deleted: Optional[bool] = Field(default=False, description="true if the item is deleted")
    dead: Optional[bool] = Field(default=False, description="true if the item is dead")

    @field_validator("hn_text_content", "original_title", mode="before")
    @classmethod
    def unescape_html(cls, v):
        if v is None:
            return None
        return html.unescape(v)
    
    @field_validator('posted_at', mode='before')
    @classmethod
    def timestamp_to_datetime(cls, v):
        if v:
            return datetime.fromtimestamp(v)
        return datetime.now()

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
    original_title: str
    original_url: Optional[str]
    score: int
    posted_at: datetime
    kids: Optional[List[int]]
    parent: Optional[int]

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
