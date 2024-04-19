"""
Tests for conversacion APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Conversacion

from conversacion.serializers import (
    ConversacionSerializer,
    ConversacionDetailSerializer,
)


CONVERSACIONES_URL = reverse('conversacion:conversacion-list')


def detail_url(conversacion_id):
    """Return conversacion detail URL."""
    return reverse('conversacion:conversacion-detail', args=[conversacion_id])


def create_conversacion(**params):
    """Helper function to create a conversacion."""
    defaults = {
        'nombre': 'Conversacion 1',
        'complejidad': 'Complejidad de la conversacion 1',
        'proposito': 'Proposito de la conversacion 1',
        'emocion': 'Emocion de la conversacion 1',
        'analogias': False,
        'empatia': 'Empatia de la conversacion 1',
        'longitudRespuesta': 'Longitud de la respuesta de la conversacion 1',
        'retroalimentacion': 'Retroalimentacion de la conversacion 1',
        'tono': 'Tono de la conversacion 1',
        'is_active': True,
    }
    defaults.update(params)

    conversacion = Conversacion.objects.create(**defaults)
    return conversacion


class PublicConversacionApiTests(TestCase):
    """Test the public conversacion API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required."""
        res = self.client.get(CONVERSACIONES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateConversacionApiTests(TestCase):
    """Test the private conversacion API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_conversaciones(self):
        """Test retrieving a list of conversaciones."""
        create_conversacion(
            nombre='Conversacion 1',
            complejidad='Complejidad de la conversacion 1',
            proposito='Proposito de la conversacion 1',
            emocion='Emocion de la conversacion 1',
            analogias=False,
            empatia='Empatia de la conversacion 1',
            longitudRespuesta='Longitud de la respuesta de la conversacion 1',
            retroalimentacion='Retroalimentacion de la conversacion 1',
            tono='Tono de la conversacion 1',
            is_active=True,
        )
        create_conversacion(
            nombre='Conversacion 2',
            complejidad='Complejidad de la conversacion 2',
            proposito='Proposito de la conversacion 2',
            emocion='Emocion de la conversacion 2',
            analogias=False,
            empatia='Empatia de la conversacion 2',
            longitudRespuesta='Longitud de la respuesta de la conversacion 2',
            retroalimentacion='Retroalimentacion de la conversacion 2',
            tono='Tono de la conversacion 2',
            is_active=True,
        )

        res = self.client.get(CONVERSACIONES_URL)

        conversaciones = Conversacion.objects.all().order_by('-id')
        serializer = ConversacionSerializer(conversaciones, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_conversacion_detail(self):
        """Test getting a conversacion detail."""
        conversacion = create_conversacion(
            nombre='Conversacion 1',
            complejidad='Complejidad de la conversacion 1',
            proposito='Proposito de la conversacion 1',
            emocion='Emocion de la conversacion 1',
            analogias=False,
            empatia='Empatia de la conversacion 1',
            longitudRespuesta='Longitud de la respuesta de la conversacion 1',
            retroalimentacion='Retroalimentacion de la conversacion 1',
            tono='Tono de la conversacion 1',
            is_active=True,
        )

        url = detail_url(conversacion.id)
        res = self.client.get(url)

        serializer = ConversacionDetailSerializer(conversacion)
        self.assertEqual(res.data, serializer.data)

    def test_create_conversacion(self):
        """Test creating a conversacion."""
        payload = {
            'nombre': 'Conversacion 1',
            'complejidad': 'Complejidad de la conversacion 1',
            'proposito': 'Proposito de la conversacion 1',
            'emocion': 'Emocion de la conversacion 1',
            'analogias': False,
            'empatia': 'Empatia de la conversacion 1',
            'longitudRespuesta': 'Longitud de la respuesta 1',
            'retroalimentacion': 'Retroalimentacion de la conversacion 1',
            'tono': 'Tono de la conversacion 1',
            'is_active': True,
        }
        res = self.client.post(CONVERSACIONES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        conversacion = Conversacion.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(conversacion, k), v)

    def test_partial_update(self):
        """Test updating a conversacion with patch."""
        conversacion = create_conversacion(
            nombre='Conversacion 1',
            complejidad='Complejidad de la conversacion 1',
            proposito='Proposito de la conversacion 1',
            emocion='Emocion de la conversacion 1',
            analogias=False,
            empatia='Empatia de la conversacion 1',
            longitudRespuesta='Longitud de la respuesta de la conversacion 1',
            retroalimentacion='Retroalimentacion de la conversacion 1',
            tono='Tono de la conversacion 1',
            is_active=True,
        )
        payload = {
            'nombre': 'Conversacion 2',
        }
        url = detail_url(conversacion.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        conversacion.refresh_from_db()
        self.assertEqual(conversacion.nombre, payload['nombre'])

    def test_full_update(self):
        """Test updating a conversacion with put."""
        conversacion = create_conversacion(
            nombre='Conversacion 1',
            complejidad='Complejidad de la conversacion 1',
            proposito='Proposito de la conversacion 1',
            emocion='Emocion de la conversacion 1',
            analogias=False,
            empatia='Empatia de la conversacion 1',
            longitudRespuesta='Longitud de la respuesta de la conversacion 1',
            retroalimentacion='Retroalimentacion de la conversacion 1',
            tono='Tono de la conversacion 1',
            is_active=True,
        )
        payload = {
            'nombre': 'Conversacion 2',
            'complejidad': 'Complejidad de la conversacion 2',
            'proposito': 'Proposito de la conversacion 2',
            'emocion': 'Emocion de la conversacion 2',
            'analogias': True,
            'empatia': 'Empatia de la conversacion 2',
            'longitudRespuesta': 'Longitud de la respuesta 2',
            'retroalimentacion': 'Retroalimentacion de la conversacion 2',
            'tono': 'Tono de la conversacion 2',
            'is_active': False,
        }
        url = detail_url(conversacion.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        conversacion.refresh_from_db()
        self.assertEqual(conversacion.nombre, payload['nombre'])
        self.assertEqual(conversacion.complejidad, payload['complejidad'])
        self.assertEqual(conversacion.proposito, payload['proposito'])
        self.assertEqual(conversacion.emocion, payload['emocion'])
        self.assertEqual(conversacion.analogias, payload['analogias'])
        self.assertEqual(conversacion.empatia, payload['empatia'])
        self.assertEqual(
            conversacion.longitudRespuesta,
            payload['longitudRespuesta']
        )
        self.assertEqual(
            conversacion.retroalimentacion,
            payload['retroalimentacion']
        )
        self.assertEqual(conversacion.tono, payload['tono'])
        self.assertEqual(conversacion.is_active, payload['is_active'])

    def test_delete_conversacion(self):
        """Test deleting a conversacion."""
        conversacion = create_conversacion(
            nombre='Conversacion 1',
            complejidad='Complejidad de la conversacion 1',
            proposito='Proposito de la conversacion 1',
            emocion='Emocion de la conversacion 1',
            analogias=False,
            empatia='Empatia de la conversacion 1',
            longitudRespuesta='Longitud de la respuesta 1',
            retroalimentacion='Retroalimentacion de la conversacion 1',
            tono='Tono de la conversacion 1',
            is_active=True,
        )
        url = detail_url(conversacion.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Conversacion.objects.filter(id=conversacion.id).exists()) # noqa
