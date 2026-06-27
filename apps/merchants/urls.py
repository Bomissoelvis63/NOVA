from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet

# Le routeur gère automatiquement les URLs pour le CRUD (ex: /payment-methods/ et /payment-methods/<id>/)
router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')

urlpatterns = [
    path('', include(router.urls)),
]