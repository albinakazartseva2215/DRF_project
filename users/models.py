from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """Класс модели User"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватарка",
        blank=True,
        null=True,
        help_text="Загрузите аватарку",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Meta класс, который задает конфигурационные параметры"""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Класс модели Payments"""

    CASH = "cash"
    TRANSFER_TO_ACCOUNT = "transfer"

    PAYMENT_METHOD_CHOICES = [
        (CASH, "Наличные"),
        (TRANSFER_TO_ACCOUNT, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    date_payment = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата платежа",
        blank=True,
        null=True,
    )
    course_payment = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="courses_payment",
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    lesson_payment = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        related_name="lessons_payment",
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма платежа",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=CASH,
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.user} - {self.amount}"
