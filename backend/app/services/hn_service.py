import asyncio
import aiohttp
from typing import Any, Dict, List, Optional, Set
from app.core.config import settings
from app.schemas.external.hn import HNRaw
from app.repositories.article_repository import article_repository
from app.core.decorators import monitor_news_ingestor

class HNService:
    def __init__(self):
        # self.top_url = settings.hn_top_url
        self.new_url = settings.hn_new_url
        self.best_url = settings.hn_best_url
        self.item_url = settings.hn_item_url
        self.limit = settings.hn_story_limit
        # limit the number of concurrent requests to the HN API
        self.sem = asyncio.Semaphore(settings.hn_fetch_concurrent_limit)

    async def _fetch_ids(self, session: aiohttp.ClientSession, url: str) -> List[int]:
        try:
            async with session.get(url) as resp:
                # checks if the HTTP response returned a successful status code (e.g. 200 OK).
                # If the response status code indicates an error (e.g. 404, 500), it will raise an aiohttp.ClientResponseError exception.
                resp.raise_for_status()
                ids = await resp.json()
                return ids[:self.limit]
        except Exception as e:
            print(f"Error fetching IDs from {url}: {e}")
            return []
    
    async def _fetch_item(self, session: aiohttp.ClientSession, id: int) -> Optional[Dict[str, Any]]:
        url = self.item_url.format(id=id)
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except Exception:
            return None
        
        if not data or data.get("type") != "story":
            return None

        try:
            story = HNRaw(**data)
            return story
        except Exception as e:
            print(f"[HNService] Error parsing story {id}: {e}")
            return None
    
    @monitor_news_ingestor(step_name="Fetch-HN")
    async def fetch_all_stories(self) -> List[HNRaw]:
        async with aiohttp.ClientSession() as session:
            task_ids = [
                # self._fetch_ids(session, self.top_url),
                self._fetch_ids(session, self.best_url),
                self._fetch_ids(session, self.new_url)
            ]
            lists_of_ids = await asyncio.gather(*task_ids)

            all_ids_set: Set[int] = set[int]()
            for ids in lists_of_ids:
                all_ids_set.update(ids)

            # prevent duplicate in db
            ids_to_fetch = [id for id in all_ids_set if not article_repository.has_article(id)]

            if not ids_to_fetch:
                return []
            
            # concurrent fetch (with semaphore)
            async def fetch_with_sem(hn_id):
                async with self.sem:
                    return await self._fetch_item(session, hn_id)
            
            tasks_items = [fetch_with_sem(hn_id) for hn_id in ids_to_fetch]

            stories = await asyncio.gather(*tasks_items)
            valid_stories = [s for s in stories if s is not None]

            return valid_stories

hn_service = HNService()