from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models
from typing import cast
from .models import PaymentMethod

User = cast(type[models.Model], get_user_model())

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class PaymentMethodSerializer(serializers.ModelSerializer):
    created_by = UserShortSerializer(read_only=True)
    updated_by = UserShortSerializer(read_only=True)

    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'merchant', 'provider_type', 'provider_name', 
            'account_identifier', 'created_by', 'updated_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'merchant', 'created_by', 'updated_by', 'created_at', 'updated_at']