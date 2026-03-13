from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .ai_chat import career_chat


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ai_assistant_api(request):
    """AI Career Advisor chat endpoint."""
    try:
        message = request.data.get("message")
        if not message:
            return Response({"error": "message is required"}, status=400)
        if not isinstance(message, str):
            return Response({"error": "message must be a string"}, status=400)
        reply = career_chat(message)
        return Response({"reply": reply})
    except Exception:
        return Response(
            {"reply": "AI assistant is temporarily unavailable."},
            status=200,
        )
