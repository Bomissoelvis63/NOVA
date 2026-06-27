from typing import cast
from django.db.models import QuerySet
from rest_framework import permissions, viewsets
from apps.security.permissions import StrictDjangoModelPermissions

from apps.accounts.models import User
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentMethodSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        StrictDjangoModelPermissions,
    ]
    queryset: QuerySet[PaymentMethod] = PaymentMethod.objects.none()
    
    def get_queryset(self) -> QuerySet[PaymentMethod]:
        user = cast(User, self.request.user)
        queryset = PaymentMethod.objects.all()

        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(merchant=user)

    def perform_create(self, serializer) -> None:
        user = cast(User, self.request.user)
        serializer.save(
            merchant=user,
            created_by=user
        )

    def perform_update(self, serializer) -> None:
        user = cast(User, self.request.user)
        serializer.save(updated_by=user)