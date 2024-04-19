"""
Views for the Conversacion APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Conversacion
from conversacion import serializers


class ConversacionViewSet(viewsets.ModelViewSet):
    """Manage conversaciones in the database."""
    serializer_class = serializers.ConversacionDetailSerializer
    queryset = Conversacion.objects.all().order_by('-id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return serializers.ConversacionSerializer

        return self.serializer_class