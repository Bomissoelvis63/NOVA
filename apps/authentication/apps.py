# apps/authentication/apps.py
# Configuration Django de l'application authentication.
# Elle declare le module responsable des flux d'authentification.
# Elle fixe le type de cle primaire par defaut pour l'app.
# Elle permet a Django de charger l'app dans INSTALLED_APPS.
# Son but est de brancher les endpoints auth dans NOVA.
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"