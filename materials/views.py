from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from materials.tasks import send_info_about_update_course
from users.permissions import IsModer, IsModerOrOwner, IsOwner


class CourseViewSet(ModelViewSet):
    """Вьюсет для реализации CRUD для курса"""

    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """Метод perform_create из Django REST Framework (DRF),
        предназначенный для кастомизации процесса создания объектов через API."""
        course = serializer.save()  # создаёт объект Course из валидных данных
        course.owner_course = self.request.user  # Привязывает текущего пользователя к полю owner
        course.save()  # Сохраняет объект с обновлёнными данными

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModer | IsOwner]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerOrOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        """При обновлении курса вызываем отложенную задачу по отправке письма подписчику курса"""
        # Сохраняем обновлённый курс
        course = serializer.save()

        # Получаем всех подписчиков курса
        subscriptions = Subscription.objects.filter(course=course).select_related("user")

        # Асинхронная рассылка каждому подписчику
        for subscription in subscriptions:
            if subscription.user.email:
                send_info_about_update_course.delay(subscription.user.email, course.course_name)


class LessonCreateApiView(CreateAPIView):
    """Дженерик для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )

    def perform_create(self, serializer):
        """При создании урока автоматически заполняется собственник - email создающего пользователя"""
        lesson = serializer.save()
        lesson.owner_lesson = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerOrOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner | ~IsModer,
    )


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerOrOwner,
    )


class SubscriptionAPIView(APIView):
    """Управление подпиской на курс"""

    def post(self, request):
        """Метод post для управления подпиской"""
        user = request.user  # получаем пользователя из self.requests
        course_id = request.data.get("course_id")  # получаем id курса из self.reqests.data
        course_item = get_object_or_404(
            Course, id=course_id
        )  # получаем объект курса из базы с помощью get_object_or_404

        # Получаем объекты подписок по текущему пользователю и курса
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
