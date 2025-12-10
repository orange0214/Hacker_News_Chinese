from fastapi import APIRouter, HTTPException, Security
from app.services.hn_service import hn_service
from app.services.extraction_service import extraction_service
from app.services.translate_service import translate_service
from app.core.news_ingestor import news_ingestor

router = APIRouter(prefix="/news", tags=["news"])

@router.post("/ingest")
async def trigger_ingestion_task():
    """
    手动触发新闻抓取与分析流程 (Task 1 测试用)
    """
    try:
        await news_ingestor.run()
        return {"message": "Ingestion task triggered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.get("/hn/demo")
async def get_hn_demo():
    try:
        stories = await hn_service.fetch_all_stories()
        urls = [story.original_url for story in stories]
        contents = await extraction_service.extract_batch(urls)
        
        # Construct the input dictionary expected by translate_service
        translation_inputs = {}
        for story in stories:
            translation_inputs[story.hn_id] = {
                "title": story.original_title,
                "hn_text": story.original_text,
                "scraped_content": contents.get(story.original_url)
            }

        summaries = await translate_service.translate_and_summarize_batch(translation_inputs)
        return {"stories": stories, "contents": contents, "summaries": summaries}

    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"抓取失败: {exc}") 