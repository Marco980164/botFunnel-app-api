"""
Views for the calificacionConversacion app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import CalificacionConversacion
from calificacionConversacion import serializers


class CalificacionConversacionViewSet(viewsets.ModelViewSet):
    """View for manage calificacionConversacion API."""
    serializer_class = serializers.CalificacionConversacionSerializer
    queryset = CalificacionConversacion.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.order_by('id')
