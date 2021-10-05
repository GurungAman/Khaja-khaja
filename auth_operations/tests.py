from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from utils import get_access_token
from django.core import mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken


# Create your tests here.


User = get_user_model()


class ChangePasswordTestCase(APITestCase):
    def setUp(self):
        self.base_url = "/api/password"
        self.user_credentials = {
            "email": "user@test.com",
            "password": "valid_password123"
        }
        self.user = User.objects.create_user(
            email=self.user_credentials['email'],
            password=self.user_credentials['password']
        )
        self.user.is_active = self.user.is_restaurant = True
        self.user.save()

        access_token = get_access_token(self.user_credentials)
        self.headers = {
            'HTTP_AUTHORIZATION': f"Bearer {access_token}"
        }

    def test_change_password_with_valid_password(self):
        """
        Provide your current and new valid password to change password.
        """
        url = f"{self.base_url}/change-password/"
        data = {
            "old_password": self.user_credentials['password'],
            "new_password": "new_password123",
            "new_password1": "new_password123"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_with_invalid_password(self):
        """
        Test case to change password by providing the wrong curretn password.
        """
        url = f"{self.base_url}/change-password/"
        data = {
            "old_password": "wrong_password",
            "new_password": "new_password123",
            "new_password1": "new_password123"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertFalse(response.data['status'])
        self.assertTrue("error" in response.data)

    def test_change_password_with_invalid_new_password(self):
        url = f"{self.base_url}/change-password/"
        data = {
            "old_password": self.user_credentials['password'],
            "new_password": "short",
            "new_password1": "short"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertFalse(response.data['status'])
        self.assertTrue("error" in response.data)

    def test_request_for_password_reset_with_valid_email(self):
        url = f"{self.base_url}/reset-password-request/"
        data = {
            "email": self.user_credentials['email']
        }
        response = self.client.post(url, data, format="json")
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_request_for_password_reset_with_invalid_email(self):
        """
        Test to send password reset mail if the email is invalid,
        i.e. the user with given email does not exist.
        """
        url = f"{self.base_url}/reset-password-request/"
        data = {
            "email": "invalid@test.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertTrue("error" in response.data)
        self.assertFalse(response.data['status'])
        self.assertEqual(response.status_code, 200)

    def test_valid_password_reset_url(self):
        """
        Checks password reset link and the mailed
        password link for their validity.
        """
        user_id_b64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)

        url = f"{self.base_url}/reset-password/{user_id_b64}/{token}/"

        response = self.client.get(url)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_passowrd_reset_link(self):
        """
        Checks if password reset link and the mailed password link is valid
        using encoded tokens and uid.
        """
        new_user = User.objects.create_user(
            email="new@user.com",
            password="test123456"
        )
        user_id_b64 = urlsafe_base64_encode(smart_bytes(new_user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        url = f"{self.base_url}/reset-password/{user_id_b64}/{token}/"
        response = self.client.get(url)
        self.assertFalse(response.data['status'])
        self.assertTrue("message" in response.data)

    def test_set_new_password(self):
        """
        Change users password by providing valid reset token and uid.
        """
        user_id_b64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        token = PasswordResetTokenGenerator().make_token(self.user)
        url = f"{self.base_url}/set-new-password/"
        data = {
            "token": token,
            "user_id_b64": user_id_b64,
            "password": "reset_password_123",
            "password1": "reset_password_123"
        }
        response = self.client.post(url, data, format="json")
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_verify_email(self):
        self.user.is_active = False
        self.user.save()
        self.assertFalse(self.user.is_active)
        access_token = AccessToken.for_user(self.user)
        access_token.set_exp(lifetime=timedelta(minutes=10))
        url = "/auth/verify-email/?token=" + str(access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        user = User.objects.get(email=self.user.email)
        self.assertTrue(user.is_active)

    def tearDown(self):
        return super().tearDown()
