"""
Views for the Pregunta APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Pregunta
from pregunta import serializers


class PreguntaViewSet(viewsets.ModelViewSet):
    """Manage preguntas in the database."""
    serializer_class = serializers.PreguntaDetailSerializer
    queryset = Pregunta.objects.all().order_by('-id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return serializers.PreguntaSerializer

        return self.serializer_class
