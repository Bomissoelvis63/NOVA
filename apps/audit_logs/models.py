# Modele de journal d'audit NOVA.
# Il stocke utilisateur, action, chemin, methode, statut et IP.
# Il indexe les champs utiles pour les recherches de securite.
# Il evite de stocker le contenu sensible des requetes.
# Son but est de tracer les activites backend importantes.
from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=12)
    status_code = models.PositiveSmallIntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["method", "path"]),
        ]

    def __str__(self):
        return f"{self.method} {self.path} {self.status_code}"
