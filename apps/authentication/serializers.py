# Serializers d'authentification de NOVA.
# Ils etendent SimpleJWT pour enrichir la reponse de login.
# Ils retournent les tokens JWT et les donnees utilisateur utiles.
# Ils evitent de dupliquer la logique de validation des credentials.
# Son but est de formater proprement les reponses de connexion.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
