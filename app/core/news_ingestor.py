from typing import List, Dict
from app.services.hn_service import hn_service
from app.services.extraction_service import extraction_service
from app.services.translate_service import translate_service
from app.repositories.article_repository import article_repository
from app.schemas.hn import HNRaw
from app.models.article import Article
from app.schemas.contexts import StoryContext
from app.core.decorators import monitor_news_ingestor
from app.core.logger import logger

class NewsIngestor:
    @monitor_news_ingestor(step_name="Ingestion-Pipeline-Main")
    async def run(self):

        # 1. Fetch all stories from HN
        raw_stories: List[HNRaw] = await hn_service.fetch_all_stories()
        if not raw_stories:
            logger.info("No new stories.")
            return {"status": "success", "total_scanned": 0, "saved_count": 0}
        
        contexts = [StoryContext(story=story) for story in raw_stories]
        logger.info(f"Processing {len(contexts)} stories...")

        # 2. Batch Extraction
        url_contexts = [ctx for ctx in contexts if ctx.story.original_url]
        if url_contexts:
            urls = [ctx.story.original_url for ctx in url_contexts]
            extracted_map = await extraction_service.extract_batch(urls)

            for ctx in url_contexts:
                content = extracted_map.get(ctx.story.original_url)
                if content is not None:
                    ctx.extracted_content = content

        # 3. Batch AI Translation and Summarization
        valid_contexts = [ctx for ctx in contexts if ctx.has_valid_content]

        if valid_contexts:
            ai_inputs: Dict[int, Dict[str, str]] = {}
            for ctx in valid_contexts:
                ai_inputs[ctx.story.hn_id] = {
                    "title": ctx.story.original_title,
                    "hn_text": ctx.story.original_text,
                    "scraped_content": ctx.extracted_content
                }

            ai_results_map = await translate_service.translate_and_summarize_batch(ai_inputs)

            for ctx in valid_contexts:
                ctx.ai_result = ai_results_map.get(ctx.story.hn_id)
        
        # 4. Save to Database
        saved_count = 0
        for ctx in valid_contexts:
            if ctx.ai_result:
                try:
                    article: Article = ctx.to_article()
                    result = article_repository.add_article(article)
                    if result:
                        saved_count += 1
                    else:
                        logger.error(f"[NewsIngestor] Failed to save story {ctx.story.hn_id}: Insert returned None")
                except Exception as e:
                    logger.error(f"[NewsIngestor] Failed to save story {ctx.story.hn_id}: {e}")

        logger.info(f"Successfully saved {saved_count} articles.")
        return valid_contexts

news_ingestor = NewsIngestor()