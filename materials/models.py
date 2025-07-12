from django.db import models


class Course(models.Model):
    """Модель курса с заданными полями и мета классом"""

    course_name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Введите название курса")
    course_preview = models.ImageField(
        upload_to="preview/",
        verbose_name="Картинка",
        help_text="Загрузите картинку",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса", blank=True, null=True
    )
    owner_course = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Владелец курса",
        help_text="Укажите владельца курса",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta класс, который задает конфигурационные параметры"""

        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    """Модель урока с заданными полями и мета классом"""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        blank=True,
        null=True,
    )
    lesson_name = models.CharField(max_length=255, verbose_name="Название урока", help_text="Введите название урока")
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    lesson_preview = models.ImageField(
        upload_to="previews/",
        verbose_name="Превью (картинка)",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Введите ссылку",
    )
    owner_lesson = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Владелец урока",
        help_text="Укажите владельца урока",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.lesson_name
