"""
Serializers for the Pregunta APIs.
"""

from rest_framework import serializers
from core.models import Pregunta


class PreguntaSerializer(serializers.ModelSerializer):
    """Serializer for Pregunta objects."""

    class Meta:
        model = Pregunta
        fields = ('id', 'conversacion', 'pregunta')
        read_only_fields = ('id',)


class PreguntaDetailSerializer(PreguntaSerializer):
    """Serializer for Pregunta detail objects."""

    class Meta(PreguntaSerializer.Meta):
        fields = PreguntaSerializer.Meta.fields + (
            'descripcion',
            'tonopregunta',
            'lenguaje'
        )
        read_only_fields = ('id',)
