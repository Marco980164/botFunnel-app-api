"""
URLs de la app instanciaConversacion
"""

from django.urls import path

from rest_framework.routers import DefaultRouter

from instanciaConversacion import views


router = DefaultRouter()
router.register('instanciaConversaciones', views.ChatBotAPIView)

app_name = 'instanciaConversacion'

urlpatterns = [
    path('', include(router.urls)),
]