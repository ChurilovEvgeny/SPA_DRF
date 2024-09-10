from http import HTTPStatus

import requests

from config.settings import TELEGRAM_API_URL


def get_chat_id(bot_token):
    """
    Создает новый чат в Telegram и возвращает его ID.
    """

    # Запрос к Telegram API для создания чата
    response = requests.get(
        f"{TELEGRAM_API_URL}/bot{bot_token}/getUpdates",
    )

    if response.status_code == HTTPStatus.OK:
        chat_data = response.json()
        if chat_data["result"]:
            return chat_data["result"][0]["message"]["chat"]["id"]
        else:
            print("Чат не найден")
            return 0
    else:
        print(f"Error: {response.status_code}")
        return 0


def send_message(message, bot_token, chat_id) -> bool:
    """
    Отправляет сообщение в чат с указанным ID чата.
    """
    if not chat_id:
        print("Chat id не указан")
        return False

    response = requests.post(
        f"{TELEGRAM_API_URL}/bot{bot_token}/sendMessage",
        params={"chat_id": chat_id, "text": message},
    )

    if response.status_code == HTTPStatus.OK:
        print("Сообщение успешно отправлено")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False


def sent_notification_in_telegram(message, bot_token) -> bool:
    return send_message(message, bot_token, get_chat_id(bot_token))
