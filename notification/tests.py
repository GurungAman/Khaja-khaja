from django.contrib.auth import get_user_model
from utils import get_access_token
from restaurant.models import FoodItems, Restaurant
from cart.models import OrderItem
from user.models import Customer
from .models import Notification as NotificationModel
from test import ProjectTestCase


# Create your tests here.
User = get_user_model()


class NotificationtestCase(ProjectTestCase):
    def setUp(self):
        super().setUp()
        self.base_url = "/api/notifications"
        password = "Valid_password123"
        user1 = User.objects.create_user(
            email="customer@test.com",
            password=password,
        )
        user2 = User.objects.create_user(
            email="restaurant@test.com",
            password=password,
        )
        user1.is_active = user2.is_active = True
        user2.is_restaurant = user1.is_customer = True
        user1.save()
        user2.save()
        self.customer = Customer.objects.create(
            customer=user1,
            first_name='name1',
            last_name="grg",
            address="pkr"
        )
        self.restaurant = Restaurant.objects.create(
            restaurant=user2,
            name='restaurant 1'
        )

        restaurant_access_token = get_access_token({
            "email": user2.email,
            "password": password
        })
        self.restaurant_headers = {
            'HTTP_AUTHORIZATION': f"Bearer {restaurant_access_token}"
        }
        self.food_item = FoodItems.objects.create(
            restaurant=self.restaurant,
            name="item 1",
            price=300
        )
        order_item = OrderItem.objects.create(
            user=self.customer,
            food_item=self.food_item,
            quantity=6
        )
        self.notification = NotificationModel.objects.create(
            user=self.restaurant,
            order_item=order_item,
            shipping_address="test city"
        )

    def test_get_notifications(self):
        """
        Test get all notifications of the restaurant.
        """
        url = f"{self.base_url}/"
        response = self.client.get(url, **self.restaurant_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['status'])

    def test_get_notification_details(self):
        """
        Get notification details along with details of customer.
        """
        url = f"{self.base_url}/{self.notification.id}/"
        response = self.client.get(url, **self.restaurant_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['status'])

    def test_mark_notification_as_read(self):
        """
        mark a notification as read as an authorized restaurant.
        """
        url = f"{self.base_url}/read/{self.notification.id}/"
        response = self.client.get(url, **self.restaurant_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['status'])
        notification = NotificationModel.objects.get(id=1)
        self.assertEqual(notification.status, "R")

    def test_mark_notification_read_as_unauthorised_user(self):
        """
        Test marking  notification as read as an unauthorized.
        """
        user = User.objects.create_user(
            email="unauth@user.com",
            password="test1234"
        )
        user.is_active = user.is_restaurant = True
        user.save()
        Restaurant.objects.create(
            restaurant=user,
            name="new restaurant"
        )
        access_token = get_access_token({
            "email": user.email,
            "password": "test1234"
        })
        headers = {
            'HTTP_AUTHORIZATION': f"Bearer {access_token}"
        }
        url = f"{self.base_url}/read/{self.notification.id}/"
        response = self.client.get(url, **headers)
        self.assertFalse(response.data['status'])
        self.assertTrue("error" in response.data)

    def tearDown(self):
        return super().tearDown()
