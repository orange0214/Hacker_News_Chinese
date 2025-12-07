from dataclasses import dataclass
from typing import Optional
from app.schemas.external.hn import HNRaw
from app.models.article import Article, AITranslatedResult

@dataclass
class StoryContext:
    story: HNRaw
    extracted_content: Optional[str] = None
    ai_result: Optional[AITranslatedResult] = None

    @property
    def has_valid_content(self) -> bool:
        return bool(self.story.original_title or self.story.original_text)
    
    def to_article(self) -> Article:
        if not self.ai_result:
            raise ValueError(f"Cannot convert story {self.story.hn_id} to Article: AI result is missing")
        
        return Article(
            # Basic info
            hn_id=self.story.hn_id,
            type=self.story.type,
            by=self.story.by,
            posted_at=self.story.posted_at,

            original_title=self.story.original_title or "Untitled",
            original_url=self.story.original_url,
            original_text=self.story.original_text,
            score=self.story.score or -1,

            # Relationship & Status
            kids=self.story.kids,
            parent=self.story.parent,
            poll=self.story.poll,
            parts=self.story.parts,
            descendants=self.story.descendants,

            deleted=self.story.deleted,
            dead=self.story.dead,

            # Content
            raw_content=self.extracted_content or "",
            image_urls=None,

            # AI-generated results
            detailed_analysis=self.ai_result,
            comment_analysis=None,
        )