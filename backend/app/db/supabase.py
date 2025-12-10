from supabase.client import create_client, Client
from app.core.config import settings

_supabase: Client | None = None

def init_supabase() -> Client:
    global _supabase
    if _supabase is None:
        _supabase = create_client(settings.supabase_url, settings.supabase_api_key)
    return _supabase

def get_supabase() -> Client:
    if _supabase is None:
        raise ValueError("Supabase client not initialized")
    return _supabase