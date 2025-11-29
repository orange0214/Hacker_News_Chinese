from fastapi import APIRouter, HTTPException, Security
from app.services.hn_service import hn_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/hn/demo")
async def get_hn_demo():
    try:
        stories = await hn_service.fetch_all_stories()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"抓取失败: {exc}")
    return {"count": len(stories), "stories": [s.dict() for s in stories]}