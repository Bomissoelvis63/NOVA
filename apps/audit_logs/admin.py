# Administration Django des audit logs NOVA.
# Elle affiche les traces API avec utilisateur, chemin, statut et IP.
# Elle permet de filtrer par methode, code HTTP et date.
# Elle aide les administrateurs a inspecter les evenements.
# Son but est de rendre l'audit consultable depuis l'admin.
from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "method", "path", "status_code", "ip_address")
    list_filter = ("method", "status_code", "created_at")
    search_fields = ("path", "user__email", "ip_address")
    readonly_fields = ("created_at",)
