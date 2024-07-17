"""
Serializers for the Reporte app.
"""
from rest_framework import serializers

from core.models import Reporte, Prospecto


class DateTimeToDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value


class ProspectoSerializer(serializers.ModelSerializer):
    """Serializer for the prospecto object."""

    class Meta:
        model = Prospecto
        fields = ('id', 'nombre', 'apellido', 'email', 'telefono', 'empresa')
        read_only_fields = ('id',)


class ReporteSerializer(serializers.ModelSerializer):
    """Serializer for the reporte object."""
    my_date_field = DateTimeToDateField(source='fechaEntrevista')
    prospecto = ProspectoSerializer()

    class Meta:
        model = Reporte
        fields = ('id', 'prospecto', 'modelo', 'calGeneral', 'my_date_field')
        read_only_fields = ('id',)
