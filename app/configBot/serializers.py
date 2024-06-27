"""
Serializers for the configBot app.
"""

from rest_framework import serializers

from core.models import ConfigBot


class ConfigBotSerializer(serializers.ModelSerializer):
    """Serializer for the configBot object."""

    class Meta:
        model = ConfigBot
        fields = ('id', 'nombre', 'proposito', 'nombreNegocio', 'descripcionNegocio', 'infoExtra')
        read_only_fields = ('id',)
