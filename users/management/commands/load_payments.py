from django.core.management.base import BaseCommand
from materials.models import Course, Lesson
from users.models import User, Payments
from decimal import Decimal
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Loads test payments into database'

    def handle(self, *args, **options):
        # Проверка существования пользователей
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR('ОШИБКА: В базе данных нет пользователей'))
            self.stdout.write(self.style.ERROR('Сначала создайте пользователей!'))
            return

        try:
            # Получаем объекты с обработкой исключений
            user1 = User.objects.get(id=2)
            user2 = User.objects.get(id=3)
            course1 = Course.objects.get(id=2)
            course2 = Course.objects.get(id=3)
            lesson1 = Lesson.objects.get(id=2)
            lesson2 = Lesson.objects.get(id=5)
        except (User.DoesNotExist, Course.DoesNotExist, Lesson.DoesNotExist) as e:
            self.stdout.write(self.style.ERROR(f'ОШИБКА: {str(e)}'))
            self.stdout.write(self.style.ERROR('Проверьте существование объектов с указанными ID'))
            return

        # Создаем тестовые платежи
        payments = [
            # Платежи за курсы
            {'user': user1, 'course_payment': course1, 'amount': Decimal('15000.00')},
            {'user': user2, 'course_payment': course2, 'amount': Decimal('18000.00')},

            # Платежи за уроки
            {'user': user1, 'lesson_payment': lesson1, 'amount': Decimal('2000.00')},
            {'user': user2, 'lesson_payment': lesson2, 'amount': Decimal('1500.00')},
        ]

        created_count = 0
        for payment in payments:
            # Проверка на дубликаты
            duplicate = False

            # Проверяем платежи за курсы
            if payment.get('course_payment'):
                duplicate = Payments.objects.filter(
                    user=payment['user'],
                    amount=payment['amount'],
                    course_payment=payment['course_payment']
                ).exists()

            # Проверяем платежи за уроки
            if not duplicate and payment.get('lesson_payment'):
                duplicate = Payments.objects.filter(
                    user=payment['user'],
                    amount=payment['amount'],
                    lesson_payment=payment['lesson_payment']
                ).exists()

            if not duplicate:
                Payments.objects.create(
                    user=payment['user'],
                    course_payment=payment.get('course_payment'),
                    lesson_payment=payment.get('lesson_payment'),
                    amount=payment['amount'],
                    payment_method=random.choice(['cash', 'transfer']),
                    date_payment=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создан платеж для {payment["user"]} на сумму {payment["amount"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Платеж уже существует: {payment["user"]} - {payment["amount"]}'))

        self.stdout.write(self.style.SUCCESS(f'Успешно создано {created_count} платежей из {len(payments)}'))
