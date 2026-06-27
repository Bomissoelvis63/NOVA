# Serializers API pour les utilisateurs NOVA.
# Ils exposent le profil utilisateur et ses groupes en lecture pour Flutter.
# Ils valident l'inscription avec mot de passe hache par Django et assignent le groupe.
# Son but est de convertir proprement users entre JSON et modeles.

# Importation des outils de typage Python pour typer statiquement le code
from typing import Any, cast
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, UserManager, PasswordResetOTP
from apps.security.fixtures import GROUPS_CONFIG


# Serializer dédié à l'affichage et à la mise à jour standard des profils utilisateurs
class UserSerializer(serializers.ModelSerializer):
    
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    # Configuration interne du serializer
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_active", "groups", "created_at")
        read_only_fields = ("id", "is_active", "groups", "created_at")



class RegisterSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True, min_length=8)
    CHOIX_GROUPES = [(nom_groupe, nom_groupe) for nom_groupe in GROUPS_CONFIG.keys()]

    group_name = serializers.ChoiceField(
        choices=CHOIX_GROUPES,
        required=True,
        write_only=True, 
        # help_text="Sélectionnez le rôle de l'utilisateur"
    )

    # Configuration interne du serializer d'inscription
    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "group_name")
        read_only_fields = ("id",)

    
    def validate_email(self, value: str) -> str:
        return value.lower()

    
    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        group_name = validated_data.pop("group_name")
        password = validated_data.pop("password")
        manager = cast(UserManager, User.objects)
        user = manager.create_user(password=password, **validated_data)
        
        
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            pass
        return user



# ==============================================================================
# SERIALIZERS POUR LA PROCÉDURE DE MOT DE PASSE OUBLIÉ (OTP)
# ==============================================================================

class PasswordResetRequestSerializer(serializers.Serializer):
    """Étape 1 : Valide l'email de l'utilisateur pour la demande d'OTP"""
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        value = value.lower().strip()
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("Aucun utilisateur actif trouvé avec cette adresse email.")
        return value


class PasswordResetVerifySerializer(serializers.Serializer):
    """Étape 2 : Valide la cohérence du code OTP saisi sur Flutter"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs.get("email", "").lower().strip()
        code = attrs.get("code", "").strip()

        # On cherche l'OTP valide le plus récent pour cet email
        otp_record = PasswordResetOTP.objects.filter(
            user__email=email, 
            code=code
        ).first()

        if not otp_record or not otp_record.is_valid:
            raise serializers.ValidationError({"code": "Code OTP invalide ou expiré."})

        # On garde l'enregistrement OTP en mémoire dans le contexte validé pour la vue
        attrs["otp_record"] = otp_record
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Étape 3 : Valide et applique le nouveau mot de passe"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value: str) -> str:
        # On applique tes règles de validation de sécurité Django natives (MinimumLength, etc.)
        validate_password(value)
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs.get("email", "").lower().strip()
        code = attrs.get("code", "").strip()

        # Double vérification pour s'assurer que l'OTP n'a pas été grillé entre-temps
        otp_record = PasswordResetOTP.objects.filter(user__email=email, code=code).first()
        if not otp_record or not otp_record.is_valid:
            raise serializers.ValidationError("La session de réinitialisation a expiré.")

        attrs["otp_record"] = otp_record
        return attrs