"""
URL mappings for the Reporte app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from reporte import views


router = DefaultRouter()
router.register('reportes', views.ReporteViewSet)

app_name = 'reporte'

urlpatterns = [
    path('', include(router.urls)),
]
