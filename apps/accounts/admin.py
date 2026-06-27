# Administration Django pour les utilisateurs NOVA.
# Elle affiche et filtre les comptes via email, statut et groupes natifs.
# Elle permet de gerer les droits et l'appartenance aux groupes depuis l'admin.
# Son but est de fournir une console admin propre pour accounts.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("email", "is_active", "is_staff", "created_at")
    list_filter = ("is_active", "is_staff", "groups")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")
    filter_horizontal = ("groups", "user_permissions")
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profil", {"fields": ("first_name", "last_name")}),
        (
            "Acces & Groupes",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "last_login")
    add_fieldsets = (
    (None, {
        "classes": ("wide",),
        "fields": (
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
        ),
    }),
)