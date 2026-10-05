from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.chatbot import generate_response
from backend.safety import check_safety, redact_sensitive_data


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

    # 1. Run safety detection on the original message
    safety_result = check_safety(request.message)

    response = None
    redacted_types = []
    message_sent_to_ai = None


    # 2. BLOCK high-confidence unsafe requests
    if safety_result["decision"] == "BLOCK":
        response = None


    # 3. Only AI messages are sent to Sarvam
    elif request.sender == "AI":

        # Remove obvious personal information BEFORE
        # sending anything to the external AI API
        safe_message, redacted_types = redact_sensitive_data(
            request.message
        )

        message_sent_to_ai = safe_message

        response = generate_response(
            safe_message
        )


    # Person A / Person B messages are NOT sent to Sarvam
    else:
        response = None


    return {
        "sender": request.sender,

        # Original message is returned for local UI display
        "message": request.message,

        "response": response,

        "safety": safety_result,

        "alert": (
            safety_result["warning"]
            if safety_result["decision"] in ["REVIEW", "BLOCK"]
            else None
        ),

        # Privacy information for explainability
        "privacy": {
            "external_ai_used": request.sender == "AI"
            and safety_result["decision"] != "BLOCK",

            "redaction_applied": len(redacted_types) > 0,

            "redacted_types": redacted_types,

            "message_sent_to_ai": message_sent_to_ai
        }
    }
    
