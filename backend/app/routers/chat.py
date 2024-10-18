from fastapi import APIRouter, Depends
from app.models.user import User
from app.models.chat import ChatMessage, ChatResponse
from app.api.deps import get_current_user
from app.services import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/chat/", response_model=ChatResponse)
async def chat(message: ChatMessage):
    response = await chatbot_service.process_message(message.message, None)
    return ChatResponse(response=response)
