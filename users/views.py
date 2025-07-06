from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    serializer_class = PaymentsSerializer

    # Настройки фильтрации и сортировки
    filterset_fields = ['course_payment', 'lesson_payment', 'payment_method']
    ordering_fields = ['date_payment']
    ordering = ['-date_payment']  # Сортировка по умолчанию
