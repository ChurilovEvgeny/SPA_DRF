import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from spa.models import Habit, Place, Action, PERIOD_EVERY_DAY
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test spa.tests.tests_habit - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class HabitTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же доступ к своим же данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.place = Place.objects.create(name="Дом")
        self.action = Action.objects.create(name="Пробежка")
        # self.course = Habit.objects.create(
        #     user=self.user,
        #     place=self.place,
        #     action=self.action,
        #     date_time=datetime.datetime(1997, 10, 19, 12, 0, 0),
        #     is_pleasant=False,
        #     related_habit=None,
        #     period=PERIOD_EVERY_DAY,
        #     reward="Бургер",
        #     time_to_complete=100,
        #     is_public=False
        # )
        self.client.force_authenticate(user=self.user)

    def add_pleasant_habit(self) -> Habit:
        habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            action=self.action,
            date_time=datetime.datetime(1997, 10, 19, 12, 0, 0),
            is_pleasant=True,
            period=PERIOD_EVERY_DAY,
            time_to_complete=100,
            is_public=False
        )
        return habit

    def test_create_valid_habit(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            # "related_habit": None,
            "period": PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(habit.place.pk, data["place"])
        self.assertEqual(habit.user, self.user)

    def test_create_not_valid_habit_time_to_complete(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 121,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 0)

    def test_create_not_valid_habit_only_related_or_reward(self):
        related_habit = self.add_pleasant_habit()
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

    def test_create_not_valid_habit_is_pleasant(self):
        related_habit = self.add_pleasant_habit()

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            # "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            # "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_not_valid_related_only_pleasant(self):
        related_habit = self.add_pleasant_habit()
        related_habit.is_pleasant = False
        related_habit.save()

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        related_habit.is_pleasant = True
        related_habit.save()

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "related_habit": related_habit.pk,
            "period": PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)