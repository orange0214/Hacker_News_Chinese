import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import api_router
from app.db.supabase import init_supabase
from app.services.extraction_service import extraction_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    supabase = init_supabase()
    app.state.supabase = supabase
    
    try:
        yield
    finally:
        # Shutdown
        app.state.supabase = None
        await extraction_service.close()

app = FastAPI(
    title="Hacker News Chinese", 
    version="1.0.0",
    docs_url="/api/docs",
    lifespan=lifespan,
)

# Mount API router
app.include_router(api_router)


def main():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()

