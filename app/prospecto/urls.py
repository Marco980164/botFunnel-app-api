"""
URL mappings for the Prospecto app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from prospecto import views


router = DefaultRouter()
router.register('prospectos', views.ProspectoViewSet)

app_name = 'prospecto'

urlpatterns = [
    path('', include(router.urls)),
]
