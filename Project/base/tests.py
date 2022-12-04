from django.test import TestCase

# from ..Project.settings import configure
from django.urls import reverse
# from django.contrib.auth.models import User

# from django.db import models
# from django.contrib.auth.models import User
# from models import Topic, Message, Room
# from django.conf import settings


# Create your tests here.

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')

        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'templates/base/login_register.html')
        self.assertTemplateUsed(response, 'base/login_register.html')


# Room.objects.all()
