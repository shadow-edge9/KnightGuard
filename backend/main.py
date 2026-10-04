from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.chatbot import generate_response
from backend.safety import check_safety

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    sender: str
    message: str

@app.get("/")
def home():
    return {
        "message": "Chatbot backend is working!"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    safety_result = check_safety(request.message)

    # High-risk message → safety alert only
    if safety_result["risk"] == "high":
        response = None

    # AI is selected → send the message to Sarvam
    elif request.sender == "AI":
        response = generate_response(request.message)

    # Person A or B → just send their message
    else:
        response = None

    return {
        "sender": request.sender,
        "message": request.message,
        "response": response,
        "safety": safety_result,
        "alert": safety_result["warning"]
        if safety_result["risk"] != "low"
        else None
    }