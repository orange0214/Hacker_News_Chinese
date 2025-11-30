import asyncio
from typing import List, Optional, Dict, Any
from app.services.hn_service import hn_service
from app.services.extraction_service import extraction_service
from app.services.translate_service import translate_service
from app.repositories.article_repository import article_repository
from app.schemas.hn import HNStoryRaw, AITranslatedResult, Article

class NewsInteger:
    async def run(self):
        print("[NewsIngestor] Starting news ingestion pipeline...")

        # 1. Fetch all stories from HN
        stories: List[HNStoryRaw] = await hn_service.fetch_all_stories()
        if not stories:
            print("[NewsIngestor] No new stories to process.")
            return
        
        print(f"[NewsIngestor] Fetched {len(stories)} new stories. Processing...")

        # 2. Prepare data for extraction and translation
        url_stories = [s for s in stories if s.original_url]
        text_stories = [s for s in stories if not s.original_url and s.hn_text_content]

        url_to_story_map = {s.original_url: s for s in url_stories}
        urls_to_fetch = list(url_to_story_map.keys())

        # 3. Batch Extraction (URLs)
        extracted_contents = await extraction_service.extract_batch(urls_to_fetch)

        final_contents_map: Dict[str, str] = {}

        for url, content in extracted_contents.items():
            if content:
                final_contents_map[url] = content
            if not content:
                print(f"[NewsIngestor] Failed to extract content for URL: {url}")
        
        