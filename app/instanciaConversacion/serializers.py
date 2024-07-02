"""
Serializers for instanciaConversacion APIs.
"""

from rest_framework import serializers

class ChatbotRequestSerializer(serializers.Serializer):
    """Serializer for chatbot request objects."""
    pregunta = serializers.CharField(max_length=255)

class ChatbotResponseSerializer(serializers.Serializer):
    respuesta = serializers.CharField(max_length=255)
    calificacion = serializers.FloatField()
