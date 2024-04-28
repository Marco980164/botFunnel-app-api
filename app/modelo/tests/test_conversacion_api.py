"""
Tests for conversacion APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Conversacion

from modelo.serializers import ConversacionSerializer


CONVERSACIONES_URL = reverse('modelo:conversacion-list')


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
