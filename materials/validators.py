from rest_framework import serializers

import re
from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_youtube_url(value):
    """Проверяет, что ссылка ведет только на YouTube"""
    if value is None:
        raise ValidationError("Поле не может быть пустым")

    # Извлекаем домен из URL
    parsed = urlparse(value)
    domain = parsed.netloc.lower()

    # Разрешенные домены YouTube
    allowed_domains = [
        'youtube.com',
        'www.youtube.com',
        'm.youtube.com',
        'youtu.be'  # короткие ссылки
    ]

    # Проверяем соответствие домена
    if not any(domain.endswith(d) for d in allowed_domains):
        raise ValidationError(
            "Разрешены только ссылки на YouTube. Обнаружен домен: " + domain
        )
