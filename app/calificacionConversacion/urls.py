"""
URL mappings for the calificacionConversacion app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from calificacionConversacion import views


router = DefaultRouter()
router.register('calificacionesConversacion',
                views.CalificacionConversacionViewSet)

app_name = 'calificacionConversacion'

urlpatterns = [
    path('', include(router.urls)),
]
