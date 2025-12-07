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
    original_text: Optional[str] = Field(default=None, alias="text", description="The comment, story or poll text. HTML.")
    score: Optional[int] = Field(default=-1, description="The story's score, or the votes for a pollopt")
    
    # Relationship fields
    kids: Optional[List[int]] = Field(default=None, description="The ids of the item's comments")
    parent: Optional[int] = Field(default=None, description="The comment's parent: either another comment or the relevant story")
    poll: Optional[int] = Field(default=None, description="The pollopt's associated poll")
    parts: Optional[List[int]] = Field(default=None, description="A list of related pollopts")
    descendants: Optional[int] = Field(default=None, description="In the case of stories or polls, the total comment count")
    
    # Status fields
    deleted: Optional[bool] = Field(default=False, description="true if the item is deleted")
    dead: Optional[bool] = Field(default=False, description="true if the item is dead")

    @field_validator("original_text", "original_title", mode="before")
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