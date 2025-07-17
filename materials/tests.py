from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test2@example.com")
        self.course = Course.objects.create(course_name="Python course", owner_course=self.user)
        self.lesson = Lesson.objects.create(lesson_name="Python django", course=self.course, owner_lesson=self.user)
        # self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("lesson_name"), self.lesson.lesson_name
        )

    def test_lesson_create(self):
        url = reverse("materials:lessons-create")
        data = {
            "lesson_name": "DRF",
            "course": self.course.pk,
            "video_url": "https://www.youtube.com/"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lessons-update", args=(self.lesson.pk,))
        data = {
            "lesson_name": "Python введение"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("lesson_name"), "Python введение"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": None,
                    "lesson_name": self.lesson.lesson_name,
                    "description": None,
                    "lesson_preview": None,
                    "course": self.course.pk,
                    "owner_lesson": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test2@example.com")
        self.course = Course.objects.create(course_name="Python course", owner_course=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """Создание подписки на курс"""
        url = reverse("materials:subscription")
        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["message"], "Подписка удалена"
        )
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user.pk,
                course=self.course.pk
            ).exists()
        )