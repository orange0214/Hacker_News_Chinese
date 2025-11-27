from app.db.supabase import get_supabase
from app.schemas.hn import Article

class ArticleRepository:
    def __init__(self):
        self.table_name = "articles"
    
    @property
    def supabase(self):
        return get_supabase()
    
    def has_article(self, hn_id: int) -> bool:
        try:
            result = self.supabase.table(self.table_name)\
                .select("id", count="exact", head=True)\
                .eq("hn_id", hn_id)\
                .execute()
            return result.count is not None and result.count > 0
        except Exception as e:
            # TODO: Log exception
            print(f"Error checking existence of article with hn_id {hn_id}: {e}")
            return False
    
    def add_article(self, article: Article) -> Article:
        try:
            data = article.model_dump(mode="json")
            response = self.supabase.table(self.table_name).insert(data).execute()
            return Article.model_validate(response.data[0])
        except Exception as e:
            # TODO: Log exception
            print(f"Error adding article: {e}")
            return None

article_repository = ArticleRepository()