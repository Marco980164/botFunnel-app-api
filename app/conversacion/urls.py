"""
URL mappings for conversacion app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from conversacion import views


router = DefaultRouter()
router.register('conversaciones', views.ConversacionViewSet)

app_name = 'conversacion'

urlpatterns = [
    path('', include(router.urls)),
]
