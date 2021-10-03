from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from user.models import Customer
from restaurant.models import Restaurant, FoodItems
from utils import get_access_token
from .models import OrderItem

# Create your tests here.
User = get_user_model()


class CartTestCase(APITestCase):
    def setUp(self):
        self.base_url = "/api/customer"
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
        self.food_item = FoodItems.objects.create(
            restaurant=self.restaurant,
            name="item 1",
            price=300
        )
        customer_access_token = get_access_token({
            "email": user1.email,
            "password": password
        })
        self.customer_headers = {
            'HTTP_AUTHORIZATION': f"Bearer {customer_access_token}"
        }
        restaurant_access_token = get_access_token({
            "email": user2.email,
            "password": password
        })
        self.restaurant_headers = {
            'HTTP_AUTHORIZATION': f"Bearer {restaurant_access_token}"
        }

    def test_create_order_item(self):
        """
        Create an order item as a customer.
        """
        url = f"{self.base_url}/order-item/"
        data = {
            "food_item": 1,
            "quantity": 5
        }
        response = self.client.post(
            url, data, format="json", **self.customer_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order_item']['food_item'], 1)
        self.assertEqual(response.data['order_item']['quantity'], 5)
        self.assertTrue(response.data['status'])
        self.assertTrue("order_item" in response.data)

    def test_create_order_item_as_Unauthorized_user(self):
        """
        Create an order item as an unauthenticated user.
        Throws an error if unautheticated.
        """
        url = f"{self.base_url}/order-item/"
        data = {
            "food_item": 1,
            "quantity": 5
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def create_order_item(self, food_item, quantity):
        """
        Helper function for creating order items.
        """
        OrderItem.objects.create(
            user=self.customer,
            food_item=food_item,
            quantity=quantity,
        )

    def test_get_order_items(self):
        """
        Get all the items in cart/order_items.
        """
        food_item2 = FoodItems.objects.create(
            restaurant=self.restaurant,
            name="item 2",
            price=1000
        )
        self.create_order_item(self.food_item, 5)
        self.create_order_item(food_item2, 3)
        url = f"{self.base_url}/order-item/"
        response = self.client.get(url, **self.customer_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['status'], True)
        self.assertEqual(response.data['count_items'], 2)
        self.assertEqual(len(response.data['order_items']),
                         response.data['count_items'])

    def test_delete_order_items(self):
        """
        Delete items from your cart/order_items.
        """
        self.create_order_item(self.food_item, 8)
        url = f"{self.base_url}/order-item/"
        data = {
            "order_items_ids": [1]
        }
        response = self.client.delete(
            url, data, format="json", **self.customer_headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_other_users_items(self):
        """
        Test to delete order items of other users.
        this raises a permission error
        """
        self.create_order_item(self.food_item, 8)
        password = "test123456"
        user = User.objects.create_user(
            email="test@test.com",
            password=password
        )
        user.is_active = user.is_customer = True
        Customer.objects.create(customer=user)
        access_token = get_access_token({
            "email": user.email,
            "password": password
        })
        headers = {'HTTP_AUTHORIZATION': f"Bearer {access_token}"}
        url = f"{self.base_url}/order-item/"
        data = {
            "order_items_ids": [1]
        }
        response = self.client.delete(
            url, data, format="json", **headers)
        self.assertFalse(response.data['status'])
        self.assertTrue("error" in response.data)

    def test_delete_all_ordered_items(self):
        """
        Delete all items from cart.
        """
        self.create_order_item(self.food_item, 8)
        url = f"{self.base_url}/order/"
        response = self.client.delete(url, **self.customer_headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_order_details(self):
        """
        Get details of all items in cart along with their toal cost and count. 
        """
        food_item2 = FoodItems.objects.create(
            restaurant=self.restaurant,
            name="item 2",
            price=1000
        )
        self.create_order_item(food_item2, 3)
        self.create_order_item(self.food_item, 5)
        url = f"{self.base_url}/order/"
        response = self.client.get(url, **self.customer_headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order_detail']['count_items'], 2)

    def test_check_out(self):
        """
        customer checkout with order items.
        notififes restaurant about customer orders after checkout.
        """
        food_item2 = FoodItems.objects.create(
            restaurant=self.restaurant,
            name="item 2",
            price=1000
        )
        self.create_order_item(food_item2, 3)
        self.create_order_item(self.food_item, 5)
        url = "/api/order/checkout/"
        data = {
            "shipping_address": "Kathmandu"
        }
        response = self.client.post(
            url, data, format="json", **self.customer_headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        return super().tearDown()
