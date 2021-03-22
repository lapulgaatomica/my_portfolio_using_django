from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Message
from .. import views
from .utils import create_and_login_superuser, create_reason, create_message


class SendMessageViewTests(TestCase):
    response = None
    message_query = None

    def setUp(self):
        create_reason()
        url = reverse('send_message')
        self.response = self.client.post(url,
                                         {'reason': '1',
                                          'name': 'Jane Doe',
                                          'email': 'jane@doe.com',
                                          'message': 'Hey Dele'},
                                         follow=True)
        self.message_query = Message.objects.get(id=1)

    def test_send_message_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_redirect_template_used(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_sent_message_template_contains_correct_html(self):
        self.assertContains(self.response, 'Your message was sent successfully, expect a feedback ASAP!!!')

    def test_message_in_database(self):
        self.assertTrue(self.message_query.name, 'Jane Doe')
        self.assertTrue(self.message_query.reason, 'I want to hire you')
        self.assertTrue(self.message_query.email, 'jane@doe.com')
        self.assertTrue(self.message_query.message, 'Hey Dele')


class MessagesReceivedViewTestsForNormalUsers(TestCase):
    response = None

    def setUp(self):
        create_message()
        url = reverse('received_messages')
        self.response = self.client.get(url, follow=True)

    def test_messages_received_view_status_code_for_non_super_user(self):
        self.assertEqual(self.response.status_code, 404)


class MessagesReceivedViewTestsForSuperUsers(TestCase):
    response = None

    def setUp(self):
        create_and_login_superuser(self.client)
        create_message()
        url = reverse('received_messages')
        self.response = self.client.get(url)

    def test_messages_received_view_status_code_for_super_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_messages_received_page_template_for_super_users(self):
        self.assertTemplateUsed(self.response, 'messages_received.html')

    def test_messages_received_page_contains_correct_html(self):
        self.assertContains(self.response, 'Jane Doe says "I want to hire you"')

    def test_messages_received_page_url_resolves_pageview(self):
        view = resolve('/message/received')
        self.assertEqual(
            view.func.__name__,
            views.MessagesReceivedView.as_view().__name__
        )