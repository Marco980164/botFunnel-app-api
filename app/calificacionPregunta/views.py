"""
Views for the calificacionPregunta app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import CalificacionPregunta
from calificacionPregunta import serializers


class CalificacionPreguntaViewSet(viewsets.ModelViewSet):
    """View for manage calificacionPregunta API."""
    serializer_class = serializers.CalificacionPreguntaSerializer
    queryset = CalificacionPregunta.objects.all().order_by('id')
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.order_by('id')
