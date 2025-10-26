"""
Minimal FastAPI application entry point
"""
from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(title="Hacker News Chinese", version="1.0.0")

# Mount API router
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

