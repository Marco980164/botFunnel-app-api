"""
Django admin customizations.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """
    Custom user admin.
    """
    ordering = ['id']
    list_display = ['id', 'email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Modelo)
admin.site.register(models.Conversacion)
admin.site.register(models.Pregunta)
admin.site.register(models.Prospecto)
admin.site.register(models.Reporte)
admin.site.register(models.CalificacionPregunta)
admin.site.register(models.CalificacionConversacion)
