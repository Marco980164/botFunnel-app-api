"""
Views for the reporte app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Reporte
from reporte import serializers


class ReporteViewSet(viewsets.ModelViewSet):
    """View for manage reporte API."""
    serializer_class = serializers.ReporteSerializer
    queryset = Reporte.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.order_by('id')
