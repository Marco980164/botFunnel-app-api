"""
Serializers for modelo APIs.
"""

from rest_framework import serializers
from core.models import Modelo


class ModeloSerializer(serializers.ModelSerializer):
    """Serializer for modelo objects."""

    class Meta:
        model = Modelo
        fields = ('id', 'nombre', 'descripcion')
        read_only_fields = ('id',)