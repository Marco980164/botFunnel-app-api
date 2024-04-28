"""
URL mappings for the calificacionPregunta app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from calificacionPregunta import views


router = DefaultRouter()
router.register('calificacionesPregunta', views.CalificacionPreguntaViewSet)

app_name = 'calificacionPregunta'

urlpatterns = [
    path('', include(router.urls)),
]
