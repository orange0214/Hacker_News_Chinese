from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.article import ArticleFilterParams, ArticleListResponse
from app.services.article_service import article_service

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/", response_model=ArticleListResponse)
async def list_articles(
    params: ArticleFilterParams = Depends()
):
    try:
        return article_service.get_article_list(params)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")