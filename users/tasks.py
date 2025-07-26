from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


@shared_task(name="users.tasks.block_inactive_users")
def block_inactive_users():
    """Блокировка пользователей, не заходивших более 30 дней"""
    # Рассчитываем дату (порог), до которой считаем пользователя активным
    threshold_date = timezone.now() - timezone.timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True).exclude(is_superuser=True)

    # Блокируем пользователей
    count = inactive_users.update(is_active=False)

    return f"Заблокировано {count} пользователей"
