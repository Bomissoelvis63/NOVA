# Configuration Django de l'application audit_logs.
# Elle declare le module responsable des traces d'audit.
# Elle fixe le type de cle primaire par defaut pour les modeles.
# Elle permet a Django de charger l'app dans INSTALLED_APPS.
# Son but est de brancher la journalisation dans NOVA.
from django.apps import AppConfig


class AuditLogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit_logs"
