"""
Serializers for instanciaConversacion APIs.
"""

from rest_framework import serializers

class ChatbotRequestSerializer(serializers.Serializer):
    """Serializer for chatbot request objects."""
    idConversacion = serializers.IntegerField()
    idPregunta = serializers.IntegerField()
    pregunta = serializers.CharField(max_length=255)
    respuesta = serializers.CharField(max_length=255)


class ChatbotResponseSerializer(serializers.Serializer):
    """Serializer for chatbot response objects."""
    pregunta = serializers.CharField(max_length=255)
    respuesta = serializers.CharField(max_length=255)
    calificacion = serializers.IntegerField()
