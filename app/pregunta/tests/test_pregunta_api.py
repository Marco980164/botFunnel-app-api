# """
# Tests fro pregunta APIs.
# """

# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse

# from rest_framework import status
# from rest_framework.test import APIClient

# from core.models import Pregunta

# from pregunta.serializers import (
#     PreguntaSerializer,
#     PreguntaDetailSerializer,
# )


# PREGUNTAS_URL = reverse('pregunta:pregunta-list')


# def create_user(email='user@example.com', password='testpass'):
#     """Helper function to create a user."""
#     return get_user_model().objects.create_user(email=email, password=password)


# def detail_url(pregunta_id):
#     """Return pregunta detail URL."""
#     return reverse('pregunta:pregunta-detail', args=[pregunta_id])


# class PublicPreguntaApiTests(TestCase):
#     """Test the public pregunta API."""

#     def setUp(self):
#         self.client = APIClient()

#     def test_auth_required(self):
#         """Test that authentication is required."""
#         res = self.client.get(PREGUNTAS_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivatePreguntaApiTests(TestCase):
#     """Test the private pregunta API."""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user()
#         self.client.force_authenticate(self.user)

#     def test_retrieve_preguntas(self):
#         """Test retrieving a list of preguntas."""
#         Pregunta.objects.create(
#             conversacion=self.conversacion,
#             pregunta='Pregunta 1',
#         )
#         Pregunta.objects.create(
#             user=self.user,
#             pregunta='Pregunta 2',
#         )

#         res = self.client.get(PREGUNTAS_URL)

#         preguntas = Pregunta.objects.all().order_by('-id')
#         serializer = PreguntaSerializer(preguntas, many=True)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)