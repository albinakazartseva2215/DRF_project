from rest_framework import serializers

from users.models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Payments"""

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "password",
            "email",
        )
