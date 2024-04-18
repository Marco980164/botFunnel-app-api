"""
Views for the Modelo APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Modelo
from modelo import serializers


class ModeloViewSet(viewsets.ModelViewSet):
    """Manage modelos in the database."""
    serializer_class = serializers.ModeloSerializer
    queryset = Modelo.objects.all().order_by('-id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
