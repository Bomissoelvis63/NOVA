# Configuration Django de l'application authorization.
# Elle declare le module qui porte roles et permissions.
# Elle fixe le type de cle primaire par defaut pour les modeles.
# Elle permet a Django d'enregistrer l'app RBAC au demarrage.
# Son but est de brancher la couche autorisation dans NOVA.
from django.apps import AppConfig


class AuthorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authorization"
