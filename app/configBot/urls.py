"""
URL mappings for the configBot app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from configBot import views


router = DefaultRouter()
router.register('configBot', views.ConfigBotViewSet)

app_name = 'configBot'

urlpatterns = [
    path('', include(router.urls)),
]