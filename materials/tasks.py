from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task(name="materials.tasks.send_info_about_update_course")
def send_info_about_update_course(email, course_name):
    """Отложенный метод отправки сообщения после обновления курса"""
    subject = f"Обновление курса: {course_name}"
    message = f"Курс '{course_name}' был обновлен. Приглашаем ознакомиться с новыми материалами!"
    send_mail(subject, message, EMAIL_HOST_USER, [email])
