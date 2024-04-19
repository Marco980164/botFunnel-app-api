"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful.
        """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized.
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123')

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_modelo(self):
        """Test creating a new modelo."""
        modelo = models.Modelo.objects.create(
            nombre='Modelo 1',
            descripcion='Descripcion del modelo 1',
        )

        self.assertEqual(str(modelo), modelo.nombre)

    def test_create_conversacion(self):
        """Test creating a new conversacion."""
        conversacion = models.Conversacion.objects.create(
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

        self.assertEqual(str(conversacion), conversacion.nombre)

    def test_create_pregunta(self):
        """Test creating a new pregunta."""
        pregunta = models.Pregunta.objects.create(
            pregunta='Pregunta 1',
            descripcion='Descripcion de la pregunta 1',
            tonopregunta='Tono de la pregunta 1',
            lenguaje='Lenguaje de la pregunta 1',
            conversacion=models.Conversacion.objects.create(
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
            ),
            is_active=True,
        )

        self.assertEqual(str(pregunta), pregunta.pregunta)


    def test_create_prospecto(self):
        """Test creating a new prospecto."""
        prospecto = models.Prospecto.objects.create(
            nombre='Prospecto 1',
            apellido='Apellido del prospecto 1',
        )

        self.assertEqual(str(prospecto), prospecto.nombre)