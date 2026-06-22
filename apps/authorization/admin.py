# Administration Django pour l'autorisation NOVA.
# Elle expose les roles et permissions dans la console admin.
# Elle facilite la recherche, le filtrage et l'association des droits.
# Elle garde la gestion RBAC accessible aux administrateurs.
# Son but est de piloter les acces sans passer par SQL.
from django.contrib import admin

from .models import Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "is_active")
    search_fields = ("key", "name")
    list_filter = ("is_active",)
    filter_horizontal = ("permissions",)
