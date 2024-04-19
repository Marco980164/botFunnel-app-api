"""
Test for modelo APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Modelo

from modelo.serializers import (
    ModeloSerializer,
    ModeloDetailSerializer,
)


MODELOS_URL = reverse('modelo:modelo-list')


def detail_url(modelo_id):
    """Return modelo detail URL."""
    return reverse('modelo:modelo-detail', args=[modelo_id])


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

    def test_get_modelo_detail(self):
        """Test getting a modelo detail."""
        modelo = create_modelo(nombre='Modelo 1', descripcion='Descripcion del modelo 1')

        url = detail_url(modelo.id)
        res = self.client.get(url)

        serializer = ModeloDetailSerializer(modelo)
        self.assertEqual(res.data, serializer.data)

    def test_create_modelo(self):
        """Test creating a modelo."""
        payload = {
            'nombre': 'Modelo 1',
            'descripcion': 'Descripcion del modelo 1',
        }
        res = self.client.post(MODELOS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        modelo = Modelo.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(modelo, k), v)

    def test_partial_update(self):
        """Test updating a modelo with patch."""
        modelo = create_modelo(nombre='Modelo 1', descripcion='Descripcion del modelo 1')
        payload = {
            'nombre': 'Modelo 2',
        }
        url = detail_url(modelo.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        modelo.refresh_from_db()
        self.assertEqual(modelo.nombre, payload['nombre'])

    def test_full_update(self):
        """Test updating a modelo with put."""
        modelo = create_modelo(nombre='Modelo 1', descripcion='Descripcion del modelo 1')
        payload = {
            'nombre': 'Modelo 2',
            'descripcion': 'Descripcion del modelo 2',
        }
        url = detail_url(modelo.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        modelo.refresh_from_db()
        self.assertEqual(modelo.nombre, payload['nombre'])
        self.assertEqual(modelo.descripcion, payload['descripcion'])

    def test_delete_modelo(self):
        """Test deleting a modelo."""
        modelo = create_modelo(nombre='Modelo 1', descripcion='Descripcion del modelo 1')
        url = detail_url(modelo.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Modelo.objects.filter(id=modelo.id).exists())
