# apps/authentication/urls.py
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
    PasswordResetConfirmView,
    PasswordResetRequestView,
    PasswordResetVerifyView,
    RefreshView,
    RegisterView,
    SessionCSRFView,
    SessionLoginView,
    SessionLogoutView,
    SessionMeView,
)

urlpatterns = [
    
    path("register/", RegisterView.as_view(), name="register"),
    
    # Routes pour la procédure de mot de passe oublié (OTP)
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/verify/", PasswordResetVerifyView.as_view(), name="password_reset_verify"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    
    
    path("t/login/", LoginView.as_view(), name="login"),
    path("t/logout/", LogoutView.as_view(), name="logout"),
    path("t/refresh/", RefreshView.as_view(), name="refresh"),
    path("t/me/", MeView.as_view(), name="me"),
    
    
    path("s/session/csrf/", SessionCSRFView.as_view(), name="session-csrf"),
    path("s/login/", SessionLoginView.as_view(), name="session-login"),
    path("s/logout/", SessionLogoutView.as_view(), name="session-logout"),
    path("s/me/", SessionMeView.as_view(), name="session-me"),
]