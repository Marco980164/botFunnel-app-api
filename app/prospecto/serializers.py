"""
Serializers for the prospecto app.
"""
from rest_framework import serializers

from core.models import Prospecto


class ProspectoSerializer(serializers.ModelSerializer):
    """Serializer for the prospecto object."""

    class Meta:
        model = Prospecto
        fields = ('id', 'nombre')
        read_only_fields = ('id',)


class ProspectoDetailSerializer(ProspectoSerializer):
    """Serializer for prospecto detail view."""

    class Meta(ProspectoSerializer.Meta):
        fields = ProspectoSerializer.Meta.fields + (
            'apellido',
            'email',
            'telefono',
            'empresa'
        )
