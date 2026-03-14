"""
AI Career Advisor Chat - Uses Google Gemini (google-genai SDK).
"""

import os
import logging

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 2000
FALLBACK_RESPONSE = "AI assistant is temporarily unavailable."


def _get_api_key():
    """Get Gemini API key from env or Django settings."""
    key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_GENAI_API_KEY")
    )
    if key:
        return key
    try:
        from django.conf import settings

        return getattr(settings, "GEMINI_API_KEY", None)
    except Exception:
        return None


def career_chat(message: str) -> str:
    """
    Send message to AI career advisor and return response.
    Handles errors safely and returns fallback on failure.
    """
    if not message or not isinstance(message, str):
        return "Please provide a valid question."

    message = message.strip()
    if not message:
        return "Please provide a valid question."

    if len(message) > MAX_MESSAGE_LENGTH:
        return f"Message is too long. Please keep it under {MAX_MESSAGE_LENGTH} characters."

    api_key = _get_api_key()
    if not api_key:
        logger.warning("No Gemini API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY.")
        return (
            "AI assistant is not configured. Please set GEMINI_API_KEY "
            "in your environment or .env file and restart the server."
        )

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        prompt = (
            "You are an AI career advisor. Give clear, concise advice about resumes, "
            "skills, and job preparation. Keep responses under 300 words.\n\n"
            f"User question: {message}"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2500,
            ),
        )

        text = None
        if hasattr(response, "text") and response.text:
            text = response.text
        elif response.candidates and len(response.candidates) > 0:
            c = response.candidates[0]
            if c.content and c.content.parts:
                text = getattr(c.content.parts[0], "text", None)

        if text and text.strip():
            return text.strip()

        return FALLBACK_RESPONSE

    except Exception as e:
        logger.exception("Gemini API error: %s", e)
        return FALLBACK_RESPONSE
    

