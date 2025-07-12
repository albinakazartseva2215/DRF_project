from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = PaymentsSerializer

    # Настройки фильтрации и сортировки
    filterset_fields = ["course_payment", "lesson_payment", "payment_method"]
    ordering_fields = ["date_payment"]
    ordering = ["-date_payment"]  # Сортировка по умолчанию


class UserCreateAPIView(CreateAPIView):
    """Класс предназначен для обработки запросов на создание нового пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Создаёт экземпляр User из валидных данных, принудительно устанавливает is_active=True
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()
