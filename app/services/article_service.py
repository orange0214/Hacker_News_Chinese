import math
from typing import List
from app.repositories.article_repository import article_repository
from app.schemas.article import ArticleFilterParams, ArticleSchema, ArticleListResponse

class ArticleService:
    def get_article_list(self, params: ArticleFilterParams) -> ArticleListResponse:
        skip = (params.page - 1) * params.size

        data, total = article_repository.get_articles(
            skip=skip,
            limit=params.size,
            sort_by=params.sort_by,
            order=params.order,
        )

        items = [ArticleSchema.model_validate(item) for item in data]

        total_pages = math.ceil(total / params.size) if params.size > 0 else 0

        return ArticleListResponse(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            total_pages=total_pages,
        )

article_service = ArticleService()