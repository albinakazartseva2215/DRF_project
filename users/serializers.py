from rest_framework import serializers
from users.models import Payments


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Payments"""

    class Meta:
        model = Payments
        fields = "__all__"
