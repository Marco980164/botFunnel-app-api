"""
Test for modelo APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modelo

from modelo.serializers import ModeloSerializer
from modelo.views import ModeloViewSet


MODELOS_URL = reverse('modelo:modelo-list')


def create_modelo(**params):
    """Helper function to create a modelo."""
    defaults = {
        'nombre': 'Modelo 1',
        'descripcion': 'Descripcion del modelo 1',
    }
    defaults.update(params)

    modelo = Modelo.objects.create(**defaults)
    return modelo


class PublicModeloApiTests(TestCase):
    """Test the public modelo API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required."""
        res = self.client.get(MODELOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateModeloApiTests(TestCase):
    """Test the private modelo API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_modelos(self):
        """Test retrieving a list of modelos."""
        create_modelo(nombre='Modelo 1', descripcion='Descripcion del modelo 1')
        create_modelo(nombre='Modelo 2', descripcion='Descripcion del modelo 2')

        res = self.client.get(MODELOS_URL)

        modelos = Modelo.objects.all().order_by('-id')
        serializer = ModeloSerializer(modelos, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
