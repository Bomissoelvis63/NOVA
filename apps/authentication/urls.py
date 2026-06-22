# Routes de l'application authentication.
# Elles mappent les endpoints publics et prives du flux auth.
# Elles gardent les chemins courts sous le prefixe global /auth/.
# Elles exposent register, login, logout, refresh et me.
# Son but est de rendre l'API d'authentification accessible.
from django.urls import path

from .views import LoginView, LogoutView, MeView, RefreshView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
]
