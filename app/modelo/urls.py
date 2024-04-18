"""
URl mappings for the modelo app
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from modelo import views


router = DefaultRouter()
router.register('modelos', views.ModeloViewSet)

app_name = 'modelo'

urlpatterns = [
    path('', include(router.urls)),
]
