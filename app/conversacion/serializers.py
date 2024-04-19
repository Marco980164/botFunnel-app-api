"""
Serializers for conversacion APIs.
"""

from rest_framework import serializers
from core.models import Conversacion


class ConversacionSerializer(serializers.ModelSerializer):
    """Serializer for conversacion objects."""

    class Meta:
        model = Conversacion
        fields = (
            'id', 'nombre', 'is_active',
        )
        read_only_fields = ('id',)


class ConversacionDetailSerializer(ConversacionSerializer):
    """Serializer for conversacion detail objects."""

    class Meta(ConversacionSerializer.Meta):
        fields = ConversacionSerializer.Meta.fields + (
            'complejidad', 'proposito', 'emocion', 'analogias', 'empatia',
            'longitudRespuesta', 'retroalimentacion', 'tono',
        )
