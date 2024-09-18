# Generated by Django 5.1 on 2024-09-18 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_user_telegram_chat_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="telegram_bot_token",
        ),
        migrations.AddField(
            model_name="user",
            name="tg_chat_id",
            field=models.IntegerField(default=0, verbose_name="Chat ID"),
        ),
        migrations.AddField(
            model_name="user",
            name="tg_name",
            field=models.CharField(
                default="", max_length=150, verbose_name="Имя в Telegram"
            ),
        ),
    ]
