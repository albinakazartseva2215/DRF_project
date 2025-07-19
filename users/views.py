from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from materials.models import Course, Lesson
from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_sessions, create_stripe_product


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = PaymentsSerializer

    # Настройки фильтрации и сортировки
    filterset_fields = ["course_payment", "lesson_payment", "payment_method"]
    ordering_fields = ["date_payment"]
    ordering = ["-date_payment"]  # Сортировка по умолчанию

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(payment.amount, product_id)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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
