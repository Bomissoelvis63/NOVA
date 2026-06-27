import uuid
from django.conf import settings
from django.db import models

class PaymentMethod(models.Model):
    
    PAYMENT_CHOICES = [
        ('MOBILE_MONEY', 'Mobile Money (Orange, MTN, Wave)'),
        ('CARD', 'Carte Bancaire'),
        ('CASH', 'Espèces à la livraison'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name="Marchand"
    )
    provider_type = models.CharField(
        max_length=20, 
        choices=PAYMENT_CHOICES, 
        verbose_name="Type de fournisseur"
    )
    provider_name = models.CharField(
        max_length=50, 
        verbose_name="Nom du service"
    )
    account_identifier = models.CharField(
        max_length=100, 
        verbose_name="Identifiant du compte / Numéro"
    )
    
    # Suivi et Traçabilité (Audit)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_catalogs",
        verbose_name="Créé par"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="updated_catalogs",
        verbose_name="Modifié par"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "PaymentMethod"
        verbose_name_plural = "PaymentMethods"

    def __str__(self):
        return f"{self.provider_type}"

