from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import validate_youtube_url


class LessonSerializer(ModelSerializer):
    """Сериализатор модели Lesson"""
    video_url = serializers.CharField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор модели Course"""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор модели Course с выводом поля количества уроков в курсе"""

    lessons_in_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, obj):
        """Определяет подписан ли текущий пользователь на курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.subscriptions.filter(user=request.user).exists()
        return False

    class Meta:
        model = Course
        fields = ("course_name", "lessons_in_course", "lessons", "is_subscribed")
