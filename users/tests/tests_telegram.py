import unittest

import responses

from config.settings import TELEGRAM_API_URL
from users.services_telegram import get_chat_id, send_message, sent_notification_in_telegram


class TestCase(unittest.TestCase):

    @responses.activate
    def test_get_chat_id_OK(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"

        body = '{"ok":true,"result":[{"update_id":24152962,"message":{"message_id":3,"from":{"id":111111111,"is_bot":false,"first_name":"Evgeny","last_name":"Churilov","username":"ChurilovEvgeny","language_code":"ru"},"chat":{"id":111111111,"first_name":"Evgeny","last_name":"Churilov","username":"ChurilovEvgeny","type":"private"},"date":1725895346,"text":"sddds"}}]}'

        responses.add(**{
            'method': responses.GET,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/getUpdates",
            'body': body,
            'status': 200,
            'content_type': 'application/json',
        })

        self.assertEqual(get_chat_id(bot_token), 111111111)

    @responses.activate
    def test_get_chat_id_empty(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"

        body = '{"ok":true,"result":[]}'

        responses.add(**{
            'method': responses.GET,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/getUpdates",
            'body': body,
            'status': 200,
            'content_type': 'application/json',
        })

        self.assertEqual(get_chat_id(bot_token), 0)

    @responses.activate
    def test_get_chat_id_not_ok(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"

        body = '{"ok":true,"result":[]}'

        responses.add(**{
            'method': responses.GET,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/getUpdates",
            'body': body,
            'status': 404,
            'content_type': 'application/json',
        })

        self.assertEqual(get_chat_id(bot_token), 0)

    @responses.activate
    def test_send_message_OK(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"
        chat_id = 111111111
        body = '{"ok":true}'

        responses.add(**{
            'method': responses.POST,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/sendMessage",
            'body': body,
            'status': 200,
            'content_type': 'application/json',
        })

        self.assertTrue(send_message("message", bot_token, chat_id))

    @responses.activate
    def test_send_message_no_chat_id(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"
        chat_id = 0

        self.assertFalse(send_message("message", bot_token, chat_id))

    @responses.activate
    def test_send_message_fail(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"
        chat_id = 111111111
        body = '{"ok":true}'

        responses.add(**{
            'method': responses.POST,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/sendMessage",
            'body': body,
            'status': 403,
            'content_type': 'application/json',
        })

        self.assertFalse(send_message("message", bot_token, chat_id))

    @responses.activate
    def test_sent_notification_in_telegram(self):
        bot_token = "somebot_tokenddfdfdfsdf655656565656"

        # Для запроса на получение chat id
        body_1 = '{"ok":true,"result":[{"update_id":24152962,"message":{"message_id":3,"from":{"id":111111111,"is_bot":false,"first_name":"Evgeny","last_name":"Churilov","username":"ChurilovEvgeny","language_code":"ru"},"chat":{"id":111111111,"first_name":"Evgeny","last_name":"Churilov","username":"ChurilovEvgeny","type":"private"},"date":1725895346,"text":"sddds"}}]}'
        responses.add(**{
            'method': responses.GET,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/getUpdates",
            'body': body_1,
            'status': 200,
            'content_type': 'application/json',
        })

        # Для отправки уведомления в Telegram
        body_2 = '{"ok":true}'
        responses.add(**{
            'method': responses.POST,
            'url': f"{TELEGRAM_API_URL}/bot{bot_token}/sendMessage",
            'body': body_2,
            'status': 200,
            'content_type': 'application/json',
        })

        self.assertTrue(sent_notification_in_telegram("message", bot_token))
