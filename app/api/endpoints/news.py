from fastapi import APIRouter, HTTPException, Security
from app.services.hn_service import hn_service
from app.services.extraction_service import extraction_service
from app.services.translate_service import translate_service

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/hn/demo")
async def get_hn_demo():
    try:
        stories = await hn_service.fetch_all_stories()
        urls = [story.original_url for story in stories]
        contents = await extraction_service.extract_batch(urls)
        # summaries = await translate_service.translate_and_summarize_batch(contents)
        return {"stories": stories, "contents": contents}

    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"抓取失败: {exc}") 