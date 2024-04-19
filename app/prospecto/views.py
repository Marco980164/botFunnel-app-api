"""
Views for the prospecto app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Prospecto
from prospecto import serializers


class ProspectoViewSet(viewsets.ModelViewSet):
    """View for manage prospecto API."""
    serializer_class = serializers.ProspectoDetailSerializer
    queryset = Prospecto.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.order_by('id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.ProspectoSerializer

        return self.serializer_class






