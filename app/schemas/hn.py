from token import OP
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import html
from typing import Optional

class HNStoryRaw(BaseModel):
    """
    This Pydantic model is responsible for:
    - Receiving the response from the HN API
    - Performing field cleaning/normalization so downstream usage is consistent
    """
    hn_id: int = Field(alis="hn_id")
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

class AIAnalysisResult(BaseModel):
    # TODO
    pass


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
    detailed_analysis: Optional[AIAnalysisResult] = None
    
    class Config:
        # allow reading data from ORM objects (if we use SQLAlchemy in the future)
        from_attributes = True 
        # when saving to the database, let Pydantic automatically convert detailed_analysis to JSON
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }