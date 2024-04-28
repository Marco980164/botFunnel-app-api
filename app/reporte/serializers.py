"""
Serializers for the Reporte app.
"""
from rest_framework import serializers

from core.models import Reporte


class ReporteSerializer(serializers.ModelSerializer):
    """Serializer for the reporte object."""

    class Meta:
        model = Reporte
        fields = ('id', 'prospecto', 'modelo', 'calGeneral', 'fechaEntrevista')
        read_only_fields = ('id',)
