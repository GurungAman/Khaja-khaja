from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from restaurant.models import Restaurant, FoodItems, Category, Tags
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
        """ Checks and return errorr if category with same name already exists. """
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
        Category.objects.create(name="category1")
        Category.objects.create(name="category2")
        Tags.objects.create(name="tag-1")
        Tags.objects.create(name="tag-2")

    def test_create_food_item(self):
        """ Creates a food item instance. """
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
