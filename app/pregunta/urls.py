"""
URL mapping for the pregunta app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from pregunta import views


router = DefaultRouter()
router.register('preguntas', views.PreguntaViewSet)

app_name = 'pregunta'

urlpatterns = [
    path('', include(router.urls)),
]
