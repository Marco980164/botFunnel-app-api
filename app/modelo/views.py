"""
Views for the Modelo APIs.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Modelo,
    Conversacion,
    Pregunta,
)
from modelo import serializers


class ModeloViewSet(viewsets.ModelViewSet):
    """Manage modelos in the database."""
    serializer_class = serializers.ModeloDetailSerializer
    queryset = Modelo.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return serializers.ModeloSerializer

        return self.serializer_class


class ConversacionViewSet(mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """Manage conversaciones in the database."""
    serializer_class = serializers.ConversacionSerializer
    queryset = Conversacion.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)


class PreguntaViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Manage preguntas in the database."""
    serializer_class = serializers.PreguntaSerializer
    queryset = Pregunta.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
