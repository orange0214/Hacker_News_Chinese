from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    supabase_url: str
    supabase_api_key: str

    # Hacker News API endpoints (top/new up to 500 stories, best stories list)
    hn_top_url: str = "https://hacker-news.firebaseio.com/v0/topstories.json"
    hn_new_url: str = "https://hacker-news.firebaseio.com/v0/newstories.json"
    hn_best_url: str = "https://hacker-news.firebaseio.com/v0/beststories.json"
    hn_item_url: str = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
    hn_poll_interval_seconds: int
    hn_story_limit: int

    # concurrent limit
    fetch_concurrent_limit: int

    # LLM API Keys
    openai_api_key: str
    deepseek_api_key: str

    # Jina
    jina_reader_base: str = "https://r.jina.ai/"
    jina_api_key: str


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()