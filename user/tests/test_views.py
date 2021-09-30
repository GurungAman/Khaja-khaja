from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        self.register_customer_url = "/api/customer/register/"
        self.token_obtain_url = "/api/token/"
        self.data = {
            "base_user": {
                "email": "test_user@test.com",
                "primary_phone_number": "12345",
                "password": "valid_password123",
                "password_1": "valid_password123"
            },
            "first_name": "test",
            "middle_name": "",
            "last_name": "grg",
            "address": "PKR"
        }
        return super().setUp()

    def resgister_customer(self):
        self.client.post(
            self.register_customer_url, self.data, format="json")

    def get_access_token(self):
        data = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        response = self.client.post(
            self.token_obtain_url, data, format="json")
        return response

    def test_create_customer_user(self):
        self.data['base_user']["password_1"] = "wrong_password"
        response = self.client.post(
            self.register_customer_url, self.data, format="json")
        self.assertFalse(response.data['status'])
        self.data['base_user']["password_1"] = "valid_password123"
        response = self.client.post(
            self.register_customer_url, self.data, format="json")
        self.assertTrue(response.data['status'])
        self.assertEqual(
            response.data['data']['email'], self.data['base_user']['email'])
        self.assertEqual(response.status_code, 200)

    def test_user_email_integrity(self):
        email = "integrity@test.com"
        user = User.objects.create_user(email=email, password="amangrg123")
        user.is_active = True
        user.is_customer = True
        user.save()
        self.data['base_user'] = email
        response = self.client.post(
            self.register_customer_url, self.data, format="json")
        self.assertFalse(response.data['status'])
        self.assertEqual(response.status_code, 200)

    def test_create_customer_with_base_data_only(self):
        data = self.data['base_user']
        response = self.client.post(
            self.register_customer_url, data, format="json")
        self.assertFalse(response.data['status'])

    def test_token_obtain_with_unverified_mail(self):
        self.resgister_customer()
        response = self.get_access_token()
        self.assertEqual(response.status_code, 401)

    def test_token_obtain_with_verified_mail(self):
        self.resgister_customer()
        data = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=data['email'])
        user.is_active = True
        user.save()
        response = self.get_access_token()
        self.assertEqual(response.status_code, 200)

    def test_get_customer_details(self):
        self.resgister_customer()
        customer_details_url = "/api/customer/"
        data = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=data['email'])
        user.is_active = True
        user.save()
        response = self.client.get(
            path=customer_details_url, format="json")
        self.assertEqual(response.status_code, 401)
        token_pair = self.get_access_token().data
        access_token = token_pair['access']
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }

        response = self.client.get(
            path=customer_details_url, **headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_details']['email'], data['email'])

    def tearDown(self):
        return super().tearDown()
