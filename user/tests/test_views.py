from django.contrib.auth import get_user_model
from user.customer_utils import customer_details
from utils import get_access_token
from test import ProjectTestCase
# Create your tests here.

User = get_user_model()


class UserTestCase(ProjectTestCase):
    def setUp(self):
        super().setUp()
        self.base_url = "/api/customer"
        self.register_customer_url = f"{self.base_url}/register/"
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

    def tearDown(self):
        return super().tearDown()

    def resgister_customer(self):
        self.client.post(
            self.register_customer_url, self.data, format="json")

    def test_create_customer_user(self):
        """ Creates a customer account on valid data. """
        response = self.client.post(
            self.register_customer_url, self.data, format="json")
        self.assertTrue(response.data['status'])
        self.assertEqual(
            response.data['data']['email'], self.data['base_user']['email'])
        self.assertEqual(response.status_code, 200)

    def test_invalid_password(self):
        """
        Check for invalid password and return an error.
        """
        self.data['base_user']["password_1"] = "wrong_password"
        response = self.client.post(
            self.register_customer_url, self.data, format="json")
        self.assertTrue("error" in response.data)
        self.assertFalse(response.data['status'])

    def test_if_email_already_exists(self):
        """
        Identifies if a user with the same email already exists.
        """
        email = self.data['base_user']['email']
        user = User.objects.create_user(email=email, password="amangrg123")
        user.is_active = True
        user.is_customer = True
        user.save()
        response = self.client.post(
            self.register_customer_url, self.data, format="json")
        self.assertTrue("error" in response.data)
        self.assertFalse(response.data['status'])
        self.assertEqual(response.status_code, 200)

    def test_create_customer_with_base_data_only(self):
        """ Create customer account without complete data. """
        data = self.data['base_user']
        response = self.client.post(
            self.register_customer_url, data, format="json")
        self.assertTrue("error" in response.data)
        self.assertFalse(response.data['status'])

    def test_token_obtain_with_unverified_mail(self):
        """ Error returned to users who are not vertified/active. """
        self.resgister_customer()
        user_credentials = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        url = f"{self.base_url}/"
        response = self.client.post(url, user_credentials, format="json")
        self.assertEqual(response.status_code, 401)

    def test_token_obtain_with_verified_mail(self):
        """
        Returns access and refresh token to users
        who have vertified their email.
        """
        self.resgister_customer()
        user_credentials = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=user_credentials['email'])
        user.is_active = True
        user.save()
        url = "/api/token/"
        response = self.client.post(url, user_credentials, format="json")
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_unvertified_customer_details(self):
        """ Return error when trying to get
        details about inactive customer. """
        self.resgister_customer()
        url = f"{self.base_url}/"
        response = self.client.get(
            path=url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_customer_details(self):
        """ Get active/vertified customer's details. """
        self.resgister_customer()
        url = f"{self.base_url}/"
        user_credentials = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=user_credentials['email'])
        user.is_active = True
        user.save()
        access_token = get_access_token(user_credentials)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }
        response = self.client.get(
            path=url, **headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)
        customer_data = customer_details(user_credentials['email'])
        self.assertEqual(response.data['customer_data'], customer_data)
        self.assertEqual(
            response.data['customer_data']['email'], user_credentials['email'])

    def test_update_customer_info(self):
        """ Update customer info. """
        self.resgister_customer()
        url = f"{self.base_url}/"
        user_credentials = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=user_credentials['email'])
        user.is_active = True
        user.save()

        access_token = get_access_token(user_credentials)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }
        update_data = {
            "primary_phone_number": "09123",
            "first_name": "test",
            "middle_name": "middle",
            "last_name": "grgg",
            "address": "new_aadress"
        }
        response = self.client.put(
            path=url, data=update_data, **headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(
            response.data['customer_data']['primary_phone_number'],
            update_data['primary_phone_number'])
        self.assertEqual(response.data['customer_data']
                         ['address'], update_data['address'])
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        """ Sets customer to inactive. """
        self.resgister_customer()
        url = f"{self.base_url}/"
        user_credentials = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=user_credentials['email'])
        user.is_active = True
        user.save()

        access_token = get_access_token(user_credentials)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }
        response = self.client.delete(
            path=url, **headers)
        self.assertTrue(response.data['status'])
        user_deleted = User.objects.get(email=user_credentials['email'])
        self.assertFalse(user_deleted.is_active)
