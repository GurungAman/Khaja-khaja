from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from utils import get_access_token

# Create your tests here.
User = get_user_model()

class NotificationtestCase(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        return super().tearDown()
