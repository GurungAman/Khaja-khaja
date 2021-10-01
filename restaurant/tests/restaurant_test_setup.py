from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from restaurant.models import Restaurant
from utils import get_access_token

User = get_user_model()


class RestaurantTestCase(APITestCase):
    """
    Access is granted only to restaurant users only
    """

    def setUp(self):
        self.base_url = "/api/restaurant/food_items"
        restaurant_credentials = {
            "email": 'restaurant@test.com',
            "password": "test12345",
        }
        restaurant_data = {
            "name": "restaurant 23",
            "license_number": "lic no. 234",
            "address": "pkr",
            "secondary_phone_number": "0098234",
            "bio": "restaurant bio"
        }
        user = User.objects.create_user(
            email=restaurant_credentials['email'],
            password=restaurant_credentials['password'])
        user.is_restaurant = True
        user.is_active = True
        user.save()
        self.restaurant = Restaurant.objects.create(
            restaurant=user,
            name=restaurant_data['name'],
            license_number=restaurant_data['license_number'],
            address=restaurant_data['address'],
            secondary_phone_number=restaurant_data['secondary_phone_number'],
            bio=restaurant_data['bio']
        )
        access_token = get_access_token(restaurant_credentials)
        self.headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }

    def tearDown(self):
        return super().tearDown()
