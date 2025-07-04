from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateApiView, LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),
]

urlpatterns += router.urls
