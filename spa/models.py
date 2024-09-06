from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}

PERIOD_DISABLE = "DISABLE"
PERIOD_EVERY_DAY = "EVERY_DAY"
PERIOD_EVERY_WEEK = "EVERY_WEEK"

PERIOD_CHOICES = {
    PERIOD_DISABLE: "Отключено",
    PERIOD_EVERY_DAY: "Ежедневно",
    PERIOD_EVERY_WEEK: "Еженедельно",
}


class Place(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название места")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Action(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название действия")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Пользователь",
        related_name="habits",
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Место",
        related_name="habits",
    )
    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Действие",
        related_name="habits",
    )

    date_time = models.DateTimeField(verbose_name="Время выполнения")

    is_pleasant = models.BooleanField(
        verbose_name="Это приятная привычка", default=False
    )

    related_habit = models.ForeignKey(
        "Habit",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Связанная привычка",
    )

    period = models.CharField(
        max_length=30,
        verbose_name="периодичность",
        choices=PERIOD_CHOICES,
        default="DISABLE",
    )

    reward = models.CharField(
        max_length=150, verbose_name="Вознаграждение", default=""
    )

    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время на выполнение, c", default=120
    )

    is_public = models.BooleanField(
        verbose_name="Признак публичности", default=False
    )

    def __str__(self):
        return f"{self.user.email}: {self.place.name}, {self.action.name}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
