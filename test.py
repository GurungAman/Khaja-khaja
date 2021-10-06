from rest_framework.test import APITestCase
from django.conf import settings


class ProjectTestCase(APITestCase):
    def setUp(self):
        settings.CELERY_TASK_ALWAYS_EAGER = True

    def tearDown(self):
        return super().tearDown()
