from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from restaurant.models import Restaurant, FoodItems, Category, Tags, Discount
from restaurant.restaurant_utils import restaurant_details
from .restaurant_test_setup import RestaurantTestCase
from utils import get_access_token


# Create your tests here.

User = get_user_model()


class RestaurantUserTestCase(APITestCase):
    def setUp(self):
        self.base_url = "/api/restaurant"
        self.resgister_restaurant_url = f"{self.base_url}/register/"
        self.data = {
            "base_user": {
                "email": "new@restaurant.com",
                "primary_phone_number": "984576",
                "password": "valid_password123",
                "password_1": "valid_password123"
            },
            "name": "restaurant 12",
            "license_number": "lic no. 12345",
            "secondary_phone_number": "98567989",
            "address": "pkr",
            "bio": "bio testing "
        }

    def tearDown(self):
        return super().tearDown()

    def resgister_restaurant(self):
        return self.client.post(
            self.resgister_restaurant_url, self.data, format="json")

    def test_create_restaurant_user(self):
        """Create a restaurant with valid data."""
        response = self.resgister_restaurant()
        self.assertTrue(response.data['status'])
        self.assertTrue("restaurant_data" in response.data)
        self.assertEqual(
            response.data['restaurant_data'][0]['email'],
            self.data['base_user']['email'])
        self.assertEqual(response.status_code, 200)

    def test_get_inactive_restaurant_detail(self):
        """
        Returns error when trying to fetch detail of
        inactive restaurant.
        """
        self.resgister_restaurant()
        url = f"{self.base_url}/1"
        response = self.client.get(url)
        self.assertTrue("error" in response.data)
        self.assertFalse(response.data['status'])

    def test_get_vertified_restaurant_details(self):
        """ Get detail of vertified/active restaurant. """
        self.resgister_restaurant()
        url = f"{self.base_url}/1"
        user = User.objects.get(email=self.data['base_user']['email'])
        user.is_active = True
        user.save()
        response = self.client.get(url)
        self.assertTrue(response.data['status'])
        restaurant = Restaurant.objects.get(restaurant=user)
        self.assertEqual(
            response.data['restaurant_detail'],
            restaurant_details([restaurant]))
        self.assertTrue("restaurant_detail" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_list_all_active_restaurants(self):
        """ Get a list of detail about all active restaurants. """
        url = f"{self.base_url}/"
        self.resgister_restaurant()
        user = User.objects.get(email=self.data['base_user']['email'])
        user.is_active = True
        user.save()
        self.data['base_user']['email'] = "another@restaurant.com"
        self.resgister_restaurant()
        user = User.objects.get(email=self.data['base_user']['email'])
        user.is_active = True
        user.save()
        response = self.client.get(url)
        self.assertTrue(response.data['status'])
        self.assertTrue("restaurant_data" in response.data)
        self.assertEqual(len(response.data['restaurant_data']), 2)

    def test_update_restaurant_detail(self):
        """ Update detail of restaurant. """
        url = f"{self.base_url}/"
        self.resgister_restaurant()
        user_credentials = {
            'email': self.data['base_user']["email"],
            'password': self.data['base_user']['password']
        }
        user = User.objects.get(email=user_credentials['email'])
        user.is_active = True
        user.save()
        update_data = {
            "name": "updated restaurant",
            "license_number": "lic no. 456",
            "secondary_phone_number": "0123",
            "address": "ktm",
            "bio": "updated bio"
        }

        access_token = get_access_token(user_credentials)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }
        response = self.client.put(
            path=url, data=update_data, format="json", **headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("restaurant_data" in response.data)
        self.assertEqual(
            response.data['restaurant_data'][0]['address'],
            update_data['address'])
        self.assertEqual(
            response.data['restaurant_data'][0]['license_number'],
            update_data['license_number'])

    def test_delete_restaurant(self):
        """ Set restaurant as inactive. """
        url = f"{self.base_url}/"
        self.resgister_restaurant()
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
        response = self.client.delete(url, **headers)
        deleted_user = User.objects.get(email=user_credentials['email'])
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)
        self.assertFalse(deleted_user.is_active)


class CategoryTestCase(RestaurantTestCase):

    def test_get_categories(self):
        """ Get list of categories. """
        url = f"{self.base_url}/category/"
        Category.objects.create(name="category1")
        Category.objects.create(name="category2")
        Category.objects.create(name="category3")
        categories = Category.objects.all()
        response = self.client.get(url)
        self.assertTrue(response.data['status'])
        self.assertEqual(categories.count(), 3)

    def test_create_category(self):
        """ Create category. """
        url = f"{self.base_url}/category/"
        data = {
            "name": "test category"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['category']['name'], data['name'])
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 1)

    def test_create_category_with_existing_name(self):
        """
        Checks and return error if category with
        same name already exists.
        """
        Category.objects.create(name='category-1')
        url = f"{self.base_url}/category/"
        data = {
            "name": "category-1"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertFalse(response.data['status'])

    def test_delete_category(self):
        """ Delete existing category. """
        Category.objects.create(name="category-1")
        url = f"{self.base_url}/category/"
        data = {
            "name": "category-1"
        }
        response = self.client.delete(url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertTrue('message' in response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_category_as_customer(self):
        """
        Returns error when tryin to create
        category as a customer.
        """
        url = f"{self.base_url}/category/"
        customer_credentials = {
            "email": 'customer@test.com',
            "password": "test12345",
        }
        user = User.objects.create_user(
            email=customer_credentials['email'],
            password=customer_credentials['password'])
        user.is_customer = True
        user.is_active = True
        user.save()
        token_pair = TokenObtainPairSerializer().validate(customer_credentials)
        access_token = token_pair['access']
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }
        data = {
            "name": "item one",
            "price": 500,
            "is_available": True
        }
        response = self.client.post(url, data, format="json", **headers)
        self.assertEqual(response.status_code, 403)


class TagsTestCase(RestaurantTestCase):

    def test_get_categories(self):
        """ Get list of tags. """
        url = f"{self.base_url}/category/"
        Tags.objects.create(name="tag 1")
        Tags.objects.create(name="tag 2")
        Tags.objects.create(name="tag 3")
        tags = Tags.objects.all()
        response = self.client.get(url)
        self.assertTrue(response.data['status'])
        self.assertEqual(tags.count(), 3)

    def test_create_tag(self):
        """ Create Tag. """
        url = f"{self.base_url}/tags/"
        data = {
            "name": "test tag"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['tag']['name'], data['name'])
        tags = Tags.objects.all()
        self.assertEqual(tags.count(), 1)

    def test_create_tag_with_existing_name(self):
        """ Returns error when creating a tag whose name already exists. """
        Tags.objects.create(name='tag-1')
        url = f"{self.base_url}/tags/"
        data = {
            "name": "tag-1"
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertFalse(response.data['status'])

    def test_delete_tag(self):
        """ Delete an existing tag. """
        Tags.objects.create(name="tag-1")
        url = f"{self.base_url}/tags/"
        data = {
            "name": "tag-1"
        }
        response = self.client.delete(url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertTrue('message' in response.data)
        self.assertEqual(response.status_code, 200)


class FoodItemsTestCase(RestaurantTestCase):
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(name="category1")
        self.category2 = Category.objects.create(name="category2")
        self.tag1 = Tags.objects.create(name="tag-1")
        self.tag2 = Tags.objects.create(name="tag-2")

    def create_test_food_item(self):
        """Helper function for creating food items instances."""
        food_item = FoodItems.objects.create(
            name="food item 1",
            restaurant=self.restaurant,
            category=self.category1,
            price=600
        )
        food_item.tags.add(self.tag1)
        food_item = FoodItems.objects.create(
            name="food item 2",
            restaurant=self.restaurant,
            category=self.category2,
            price=1000
        )
        food_item.tags.add(self.tag2)

    def test_create_food_item(self):
        """ Test for creating food item instance. """
        url = f"{self.base_url}/"
        data = {
            "category": 1,
            "tags": [],
            "name": "item one",
            "price": 500
        }
        response = self.client.post(url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("food_item" in response.data)
        self.assertEqual(response.data['food_item'][0]['name'], data['name'])

    def test_get_food_items_by_name(self):
        """Get items with their names."""
        self.create_test_food_item()
        url = f"{self.base_url}/"
        params = {
            "name": "food item 1"
        }
        response = self.client.get(url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['food_items']), 1)
        self.assertTrue(response.data['status'])

    def test_get_food_items_by_category(self):
        """Get items with category name."""
        self.create_test_food_item()
        url = f"{self.base_url}/"
        params = {
            "category": "category1"
        }
        response = self.client.get(url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['food_items']), 1)
        self.assertTrue(response.data['status'])

    def test_get_food_items_by_price(self):
        """Get items with based on their price."""
        self.create_test_food_item()
        url = f"{self.base_url}/"
        params = {
            "min_price": 700,
            "max_price": 1100
        }
        response = self.client.get(url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['food_items']), 1)
        self.assertTrue(response.data['status'])

    def test_get_food_item_detail(self):
        """Get item details."""
        self.create_test_food_item()
        url = f"{self.base_url}/2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['status'])
        self.assertTrue("food_item" in response.data)
        self.assertEqual(response.data['food_item']['id'], 2)

    def test_update_food_item(self):
        """
        Update item details by restaurant who created
        the food item instance.
        """
        self.create_test_food_item()
        data = {
            "category": 2,
            "name": "updated name",
            "remove_tags": [2],
            "price": 100
        }
        url = f"{self.base_url}/2"
        response = self.client.put(url, data, format="json", **self.headers)
        self.assertTrue("food_item" in response.data)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['food_item']['name'], data['name'])
        self.assertEqual(response.data['food_item']['price'], data['price'])

    def test_update_food_item_by_unauthorized_restaurant(self):
        """
        Test updating item details by unauhtorized restaurant.
        """
        self.create_test_food_item()
        user_credentials = {
            "email": "unauth@restaurant.com",
            "password": "newpassword123"
        }
        user = User.objects.create_user(
            email=user_credentials['email'],
            password=user_credentials['password']
        )
        user.is_active = user.is_restaurant = True
        user.save()
        Restaurant.objects.create(
            restaurant=user,
            name="Restaurant 123",
            license_number="lic 122345",
            address="address pkr",
            secondary_phone_number="0912456",
            bio="bio 123"
        )
        data = {
            "name": "updated name",
            "price": 100
        }
        url = f"{self.base_url}/2"
        access_token = get_access_token(data=user_credentials)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }

        response = self.client.put(url, data, format="json", **headers)
        self.assertFalse(response.data['status'])
        self.assertTrue('error' in response.data)

    def test_delete_food_item(self):
        """
        Test item deletion.
        """
        self.create_test_food_item()
        url = f"{self.base_url}/2"
        response = self.client.delete(url, format="json", **self.headers)
        self.assertTrue("message" in response.data)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)


class DiscountTestCase(RestaurantTestCase):
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(name="category1")
        self.food_item = FoodItems.objects.create(
            name="food item 1",
            restaurant=self.restaurant,
            category=self.category1,
            price=600
        )
        self.discount_url = f"{self.base_url}/{self.food_item.id}/discount/"

    def test_create_discount(self):
        """
        Test for creation of discount for food item by
        an authorized restaurant user.
        """
        data = {
            "discount_type": "amount",
            "discount_amount": 20
        }
        response = self.client.post(
            self.discount_url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.data['food_item']['id'], self.food_item.id)
        self.assertEqual(response.status_code, 200)

    def test_create_discount_greater_than_price(self):
        """
        Test for creating discount that is greater than actual
        price of the item.
        This returns a validatione error.
        """
        data = {
            "discount_type": "amount",
            "discount_amount": 1000
        }
        response = self.client.post(
            self.discount_url, data, format="json", **self.headers)
        self.assertTrue("error" in response.data)
        self.assertFalse(response.data['status'])

    def test_create_discount_by_unauthorized_user(self):
        """
        Creating discount for food item as an unauthorized users.
        """
        user_credentials = {
            "email": "unauth@restaurant.com",
            "password": "newpassword123"
        }
        user = User.objects.create_user(
            email=user_credentials['email'],
            password=user_credentials['password']
        )
        user.is_active = user.is_restaurant = True
        user.save()
        Restaurant.objects.create(
            restaurant=user,
            name="Restaurant 123"
        )
        access_token = get_access_token(data=user_credentials)
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {access_token}"
        }
        data = {
            "discount_type": "percentage",
            "discount_amount":  50
        }
        response = self.client.post(
            self.discount_url, data, format="json", **headers)
        self.assertFalse(response.data['status'])
        self.assertTrue("error" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_discount(self):
        """
        Udating discount for food item if it already exists.
        Creates a new discount instance if it does not exiist.
        """
        Discount.objects.create(
            food_item=self.food_item,
            discount_type="amount",
            discount_amount=20
        )
        data = {
            "discount_type": "percentage",
            "discount_amount":  30
        }
        response = self.client.post(
            self.discount_url, data, format="json", **self.headers)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['food_item']
                         ['discount_type'], data["discount_type"])
        self.assertTrue("message" in response.data)

    def test_delete_discount(self):
        Discount.objects.create(
            food_item=self.food_item,
            discount_type="amount",
            discount_amount=20
        )
        response = self.client.delete(self.discount_url,  **self.headers)
        self.assertTrue(response.data['status'])
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, 200)

