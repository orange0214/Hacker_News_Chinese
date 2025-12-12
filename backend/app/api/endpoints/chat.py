from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.chat_service import chat_service
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def chat(request: ChatRequest):
    return StreamingResponse(
        chat_service.stream_chat(
            request.article_id, 
            request.message, 
            request.history
        ),
        media_type="text/event-stream"
    )