from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db, close_db
from app.routers import anime_router, users_router, ratings_router, recommendations_router, chat_router
from app.services import ChatbotService, NLPService
from app.models.user import User
from app.models.chat import ChatMessage, ChatResponse
from app.api.deps import get_current_user

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

chatbot_service = ChatbotService()

@app.on_event("startup")
async def startup_db_client():
    await init_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()

app.include_router(anime_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(ratings_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to AniBot!"}

@app.post("/api/v1/chat/", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        response = await chatbot_service.process_message(message.message, None)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
