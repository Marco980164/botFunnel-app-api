"""
Test for Prospecto APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Prospecto

from prospecto.serializers import (
    ProspectoSerializer,
    ProspectoDetailSerializer
)


PROSPECTOS_URL = reverse('prospecto:prospecto-list')

def detail_url(prospecto_id):
    """Create and return a detail URL for a prospecto."""
    return reverse('prospecto:prospecto-detail', args=[prospecto_id])


def create_prospecto(nombre, **params):
    """Create a new prospecto."""
    defaults = {
        'apellido': 'Apellido',
        'email': 'prospecto@example.com',
        'telefono': '1234567890',
        'empresa': 'Empresa',
    }
    defaults.update(params)

    prospecto = Prospecto.objects.create(nombre=nombre, **defaults)
    return prospecto

def create_user(**params):
    """Create a new user."""
    return get_user_model().objects.create_user(**params)


class PublicProspectoApiTests(TestCase):
    """Test the public prospecto API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PROSPECTOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProspectoApiTests(TestCase):
    """Test authenticated prospecto API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_prospectos(self):
        """Test retrieving a list of prospectos."""
        create_prospecto(nombre='Prospecto 1')
        create_prospecto(nombre='Prospecto 2')

        res = self.client.get(PROSPECTOS_URL)

        prospectos = Prospecto.objects.all().order_by('id')
        serializer = ProspectoSerializer(prospectos, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_get_prospectos_detail(self):
        """Test getting a prospecto detail."""
        prospecto = create_prospecto(nombre='Prospecto 1')

        url = detail_url(prospecto.id)
        res = self.client.get(url)

        serializer = ProspectoDetailSerializer(prospecto)

        self.assertEqual(res.data, serializer.data)

    def test_create_prospecto(self):
        """Test creating a new prospecto."""
        payload = {
            'nombre': 'Prospecto #',
            'apellido': '5',
            'email': 'prospecto@example.com',
            'telefono': '1234567890',
            'empresa': 'Empresa fantasma',
        }
        res = self.client.post(PROSPECTOS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        prospecto = Prospecto.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(v, getattr(prospecto, k))
        self.assertEqual(prospecto.nombre, payload['nombre'])

    def test_partial_update(self):
        """Test partial update of a prospecto."""
        prospecto_apellido = 'Apellido del prospecto'
        prospecto = create_prospecto(nombre='Prospecto 1', apellido=prospecto_apellido)

        payload = {'nombre': 'Nuevo nombre del prospecto'}
        url = detail_url(prospecto.id)
        res = self.client.patch(url, payload)


        self.assertEqual(res.status_code, status.HTTP_200_OK)
        prospecto.refresh_from_db()
        self.assertEqual(prospecto.nombre, payload['nombre'])
        self.assertEqual(prospecto.apellido, prospecto_apellido)


    def test_full_update(self):
        """Test full update of a prospecto."""
        prospecto = create_prospecto(
            nombre='Prospecto 1',
            apellido='Apellido del prospecto',
            email='prospectomail@example.com',
            telefono='1234567890',
            empresa='Empresa fantasma'
            )

        payload = {
            'nombre': 'Nuevo nombre del prospecto',
            'apellido': 'Nuevo apellido del prospecto',
            'email': 'nuevoprospectomail@example.com',
            'telefono': '0987654321',
            'empresa': 'Empresa fantasma nueva',
        }
        url = detail_url(prospecto.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        prospecto.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(v, getattr(prospecto, k))
        self.assertEqual(prospecto.nombre, payload['nombre'])


    def test_delete_prospecto(self):
        """Test deleting a prospecto."""
        prospecto = create_prospecto(nombre='Prospecto 1')

        url = detail_url(prospecto.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Prospecto.objects.filter(id=prospecto.id).exists())