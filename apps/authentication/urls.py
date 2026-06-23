# Routes de l'application authentication.
# Elles separent les flux JWT et session serveur.
# Elles gardent les chemins courts sous le prefixe global /auth/.
# Elles exposent register, login, logout, refresh, me et session/*.
# Son but est de rendre les strategies d'auth explicites.
from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    MeView,
    RefreshView,
    RegisterView,
    SessionCSRFView,
    SessionLoginView,
    SessionLogoutView,
    SessionMeView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("session/csrf/", SessionCSRFView.as_view(), name="session-csrf"),
    path("session/login/", SessionLoginView.as_view(), name="session-login"),
    path("session/logout/", SessionLogoutView.as_view(), name="session-logout"),
    path("session/me/", SessionMeView.as_view(), name="session-me"),
]
