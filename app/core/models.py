"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for user profiles."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Modelo(models.Model):
    """Modelo object."""
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    conversaciones = models.ManyToManyField('Conversacion')

    def __str__(self):
        return self.nombre


class Conversacion(models.Model):
    """Conversacion object."""
    nombre = models.CharField(max_length=255)
    complejidad = models.CharField(max_length=255)
    proposito = models.CharField(max_length=255)
    emocion = models.CharField(max_length=255)
    analogias = models.BooleanField(default=False)
    empatia = models.CharField(max_length=255)
    longitudRespuesta = models.CharField(max_length=255)
    retroalimentacion = models.CharField(max_length=255)
    tono = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Pregunta(models.Model):
    """Pregunta object."""
    pregunta = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tonopregunta = models.CharField(max_length=255)
    lenguaje = models.CharField(max_length=255)
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.pregunta


class Prospecto(models.Model):
    """Prospecto object."""
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
