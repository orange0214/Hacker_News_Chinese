import asyncio
import httpx
from typing import Optional, List
from app.core.config import settings

class ExtractionService:
    def __init__(self):
        self.jina_reader_base = settings.jina_reader_base
        self.headers = {}
        if settings.jina_api_key:
            self.headers["Authorization"] = f"Bearer {settings.jina_api_key}"
        self.sem = asyncio.Semaphore(settings.fetch_concurrent_limit)
        
    
    async def extract_url(self, url: str) -> Optional[str]:
        # Extract clean Markdown content from the URL by using Jina Reader API
        if not url:
            return None
        
        target_url = f"{self.jina_reader_base}{url}"

        try:
            async  with self.sem:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(target_url, headers=self.headers)
                    # raise an exception if the response status code is not 200-299
                    response.raise_for_status()
                    return response.text
        except Exception as e:
            print(f"[ExtractionService] Error extracting URL {url}: {e}")
            return None
    
    async def extract_batch(self, urls: List[str]) -> List[Optional[str]]:
        # concurrently extract content from multiple URLs
        print(f"[ExtractionService] Extracting batch of {len(urls)} URLs...")

        tasks = [self.extract_url(url) for url in urls]

        results = await asyncio.gather(*tasks)

        return dict(zip(urls, results))

extraction_service = ExtractionService()