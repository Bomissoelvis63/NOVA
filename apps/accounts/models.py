# Modeles utilisateur du projet NOVA.
# Ils definissent un User custom base sur l'email et un UUID.
# Ils gerent la creation d'utilisateurs et superutilisateurs.
# Ils s'appuient desormais sur PermissionsMixin pour la gestion native des groupes.
# Son but est de centraliser l'identite utilisateur sans logique RBAC redondante.
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random
from datetime import timedelta
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est requise.")
        if not password:
            raise ValueError("Le mot de passe est obligatoire.")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta(AbstractBaseUser.Meta):
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
    
    
# ==============================================================================
#  NOUVEAU MODELE POUR GÉRER L'OTP DU MOT DE PASSE OUBLIÉ
# ==============================================================================
class PasswordResetOTP(models.Model):
    # On lie l'OTP à ton modèle User ci-dessus via une clé étrangère
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_otps",
        verbose_name="Utilisateur"
    )
    code = models.CharField(max_length=6, verbose_name="Code OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    is_used = models.BooleanField(default=False, verbose_name="Utilisé")
    expires_at = models.DateTimeField(verbose_name="Expire le")

    class Meta:
        verbose_name = "OTP de réinitialisation"
        verbose_name_plural = "OTP de réinitialisation"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Génère automatiquement un code à 6 chiffres à la création
        if not self.code:
            self.code = f"{random.randint(100000, 999999)}"
        
        # Définit l'expiration à +10 minutes automatiquement
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
            
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        # Un code est valide s'il n'a pas été utilisé et si l'heure actuelle n'a pas dépassé l'expiration
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return f"OTP {self.code} - {self.user.email}"
