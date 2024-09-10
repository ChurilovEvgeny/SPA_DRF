from celery import shared_task
from django.utils import timezone

from spa.models import Habit
from users.services_telegram import sent_notification_in_telegram


@shared_task
def send_user_notification_in_telegram():
    habits = Habit.objects.filter(date_time_next_sent__lte=timezone.now().replace(second=0, microsecond=0))
    print(habits.query)
    for habit in habits:
        message = (f"Пора выполнять привычку!\n"
                   f"Место: {habit.place}.\n"
                   f"Действие: {habit.action}.\n"
                   f"На выполнение {habit.time_to_complete} секунд.\n"
                   f"А в качестве награды { habit.related_habit if habit.related_habit else habit.reward }!!!")
        token = habit.user.telegram_bot_token
        sent_notification_in_telegram(message, token)

        habit.set_next_execution_time()
