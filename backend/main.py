from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.chatbot import (
    generate_response,
    normalize_to_english
)

from backend.safety import (
    check_safety,
    redact_sensitive_data
)


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


def choose_stronger_result(original_result, normalized_result):

    priority = {
        "NO_WARNING": 0,
        "REVIEW": 1,
        "BLOCK": 2
    }

    if (
        priority.get(normalized_result["decision"], 0)
        > priority.get(original_result["decision"], 0)
    ):
        return normalized_result

    return original_result


@app.post("/chat")
def chat(request: ChatRequest):

    original_message = request.message


    # ------------------------------------------
    # STEP 1: Local safety check
    # ------------------------------------------

    original_safety = check_safety(
        original_message
    )


    # ------------------------------------------
    # STEP 2: Remove PII BEFORE Sarvam
    # ------------------------------------------

    safe_message, redacted_types = (
        redact_sensitive_data(
            original_message
        )
    )


    normalized_message = safe_message
    source_language = None
    normalization_used = False
    external_ai_used = False


    # ------------------------------------------
    # STEP 3: Already unsafe?
    # Don't send to external API
    # ------------------------------------------

    if original_safety["decision"] == "BLOCK":

        safety_result = original_safety


    else:

        # --------------------------------------
        # STEP 4: Sarvam language normalization
        # Hinglish / Indic -> English
        # --------------------------------------

        (
            normalized_message,
            source_language,
            normalization_used
        ) = normalize_to_english(
            safe_message
        )

        # Translation call uses external AI
        if safe_message and len(safe_message) <= 1000:
            external_ai_used = True


        # Safety check on normalized text
        normalized_safety = check_safety(
            normalized_message
        )


        # Keep more serious result
        safety_result = choose_stronger_result(
            original_safety,
            normalized_safety
        )


    response = None


    # ------------------------------------------
    # STEP 5: AI chatbot response
    # ------------------------------------------

    if (
        request.sender == "AI"
        and safety_result["decision"] != "BLOCK"
    ):

        response = generate_response(
            safe_message
        )

        external_ai_used = True


    # ------------------------------------------
    # STEP 6: Return result
    # ------------------------------------------

    return {

        "sender": request.sender,

        "message": original_message,

        "response": response,

        "safety": safety_result,

        "alert": (
            safety_result["warning"]
            if safety_result["decision"]
            in ["REVIEW", "BLOCK"]
            else None
        ),


        # Privacy information
        "privacy": {

            "external_ai_used":
                external_ai_used,

            "redaction_applied":
                len(redacted_types) > 0,

            "redacted_types":
                redacted_types,

            "message_sent_to_ai":
                safe_message
                if external_ai_used
                else None,

            "raw_pii_sent_to_external_ai":
                False
        },


        # Language information
        "language": {

            "normalization_used":
                normalization_used,

            "source_language":
                source_language,

            "normalized_for_safety":
                normalized_message
                if normalization_used
                else None
        }
    }
