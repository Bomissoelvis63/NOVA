# Configuration Django de l'application accounts.
# Elle declare le chemin Python complet de l'app utilisateur.
# Elle fixe le type de cle primaire par defaut pour les modeles.
# Elle permet a Django d'enregistrer correctement l'app au demarrage.
# Son but est de brancher le module users dans le projet NOVA.
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
