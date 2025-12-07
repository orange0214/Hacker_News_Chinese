from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SortField(str, Enum):
    POSTED_AT = "posted_at"
    SCORE = "score"
    AI_SCORE = "ai_score"

class SortOrder(str, Enum):
    DESC = "desc"
    ASC = "asc"

# --- Request Models (Query Params) ---
class ArticleFilterParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Page size")
    sort_by: SortField = Field(default=SortField.POSTED_AT, description="Sort field")
    order: SortOrder = Field(default=SortOrder.DESC, description="Sort order")

# --- Response Models (DTOs) ---
