"""
Serializers for the calificacionPregunta app.
"""
from rest_framework import serializers

from core.models import CalificacionPregunta


class CalificacionPreguntaSerializer(serializers.ModelSerializer):
    """Serializer for the calificacionPregunta object."""

    class Meta:
        model = CalificacionPregunta
        fields = ('id', 'pregunta', 'prospecto', 'calificacion')
        read_only_fields = ('id',)
