from app.db.supabase import get_supabase
from app.schemas.hn import Article

class ArticleRepository:
    def __init__(self):
        self.table_name = "articles"
    
    @property
    def supabase(self):
        return get_supabase()
    
    def has_article(self, hn_id: int) -> bool:
        """
        Check whether an article with the given Hacker News ID exists in the database.

        Args:
            hn_id (int): Hacker News article ID.

        Returns:
            bool: True if the article exists, False otherwise.
        """
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
        



article_repository = ArticleRepository()