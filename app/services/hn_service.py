import asyncio
import aiohttp
from typing import Any, Dict, List, Optional, Set
from app.core.config import settings
from app.schemas.hn import HNStoryRaw

class HackerNewsClient:
    def __init__(self):
        self.top_url = settings.hn_top_url
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
            story = HNStoryRaw(**data)
            return story
        except Exception as e:
            print(f"[HNStory] Error parsing story {id}: {e}")
            return None
    
    async def fetch_all_stories(self) -> List[HNStoryRaw]:
        """
        Get all IDs from Top/Best/New -> Memory deduplication -> Concurrent fetch details
        (temporarily remove Supabase database deduplication logic)
        """
        async with aiohttp.ClientSession() as session:
            print("[HN] Fetching all stories from Top, Best, New...")
            task_ids = [
                self._fetch_ids(session, self.top_url),
                self._fetch_ids(session, self.best_url),
                self._fetch_ids(session, self.new_url)
            ]
            lists_of_ids = await asyncio.gather(*task_ids)

            all_ids_set: Set[int] = set()
            for ids in lists_of_ids:
                all_ids_set.update(ids)

            # TODO
            # Supabase database deduplication logic
            
            ids_to_fetch = list(all_ids_set)
            print(f"[HN] Fetching {len(ids_to_fetch)} stories from Top, Best, New...")

            if not ids_to_fetch:
                return []
            
            # concurrent fetch (with semaphore)
            async def fetch_with_sem(hn_id):
                async with self.sem:
                    return await self._fetch_item(session, hn_id)
            
            tasks_items = [fetch_with_sem(hn_id) for hn_id in ids_to_fetch]

            print(f"[HN] Starting concurrent fetch for {len(tasks_items)} items...")
            stories = await asyncio.gather(*tasks_items)
            valid_stories = [s for s in stories if s is not None]

            print(f"[HN] Successfully fetched {len(valid_stories)} valid stories.")
            return valid_stories

hn_client = HackerNewsClient()