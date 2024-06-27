"""
Views for the configBot app.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import ConfigBot
from configBot import serializers


class ConfigBotViewSet(viewsets.ModelViewSet):
    """View for manage configBot API."""
    serializer_class = serializers.ConfigBotSerializer
    queryset = ConfigBot.objects.all().order_by('id')
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.order_by('id')