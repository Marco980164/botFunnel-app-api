"""
Serializers for the calificacionConversacion app.
"""
from rest_framework import serializers

from core.models import CalificacionConversacion


class CalificacionConversacionSerializer(serializers.ModelSerializer):
    """Serializer for the calificacionConversacion object."""

    class Meta:
        model = CalificacionConversacion
        fields = ('id', 'conversacion', 'reporte', 'calificacion')
        read_only_fields = ('id',)
