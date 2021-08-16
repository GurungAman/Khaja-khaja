import json
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from .models import Category, Tags, FoodItems, Restaurant, Discount
from .serializers import CategorySerializer, TagsSerializer, RestaurantSerializer, UpdateRestaurantSerializer
from .restaurant_utils import food_items_details, get_food_items, restaurant_details, add_tags_to_food_item
from permissions import IsRestaurantOrReadOnly
from .decorators import restaurant_owner_only
from user.serializers import CreateBaseUserSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register_restaurant(request):
    # {
    #     "base_user": {
    #         "email": "new1@test.com",
    #         "primary_phone_number": "asdklfju",
    #         "password": "amangrg123",
    #         "password_1": "amangrg123"
    #     },
    #     "name": "test",
    #     "logo": __file__,
    #     "license_number": "grgg",
    #     "address": "pkr",
    #     "secondary_phone_number": "",
    #     "bio": ""
    # }
    response = {
        'status': False
    }
    try:
        customer_data = request.data
        base_user_serializer = CreateBaseUserSerializer(
            data=customer_data['base_user'])
        restaurant_serializer = RestaurantSerializer(data=customer_data)
        if restaurant_serializer.is_valid(raise_exception=False) and base_user_serializer.is_valid(raise_exception=False):
            base_user_serializer.save(customer_data['base_user'])
            data = restaurant_serializer.data
            restaurant_serializer.save(data)
            response['data'] = data
            response['status'] = True
        else:
            response['error'] = restaurant_serializer.errors
    except Exception as e:
        response['error'] = f"{e.__class__.__name__}"
    return Response(response)


@api_view(['GET'])
@permission_classes([AllowAny])
def restaurant_detail(request, pk):
    response = {
        'status': False
    }
    try:
        restaurant = Restaurant.objects.get(id=pk)
        if restaurant.restaurant.is_active:
            response['restaurant_detail'] = restaurant_details([restaurant])
            response['status'] = True
        else:
            response['error'] = f'Restaurant {restaurant.name} is not active'
    except Exception as e:
        response['error'] = f"{e.__class__.__name__}"
    return Response(response)


class RestaurantList(APIView):
    response = {
        'status': False,
    }
    permission_classes = [IsRestaurantOrReadOnly]

    def get(self, request):
        try:
            restaurants = Restaurant.objects.filter(restaurant__is_active=True)
            self.response['restaurant'] = restaurant_details(restaurants)
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)

    def put(self, request):
        user = request.user
        data = request.data
        try:
            restaurant = Restaurant.objects.get(restaurant=user)
            restaurant_serializer = UpdateRestaurantSerializer(data=data)
            if restaurant_serializer.is_valid(raise_exception=False):
                restaurant_serializer.save(
                    instance=restaurant, validated_data=data)
                self.response['restaurant'] = restaurant_details([restaurant])
                self.response['status'] = True
            else:
                self.response['error'] = restaurant_serializer.errors
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)

    def delete(self, request):
        user = request.user
        try:
            restaurant = Restaurant.objects.get(restaurant=user)
            restaurant.restaurant.is_active = False
            restaurant.save()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class CategoryList(APIView):
    # create, delete category and get all categories
    permission_classes = [IsRestaurantOrReadOnly]
    response = {
        'status': False
    }

    def get(self, request):
        try:
            categories = Category.objects.all()
            category_serializer = CategorySerializer(categories, many=True)
            self.response['category'] = category_serializer.data
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f'{e.__class__.__name__}'
        return Response(self.response)

    def post(self, request):
        try:
            category_serializer = CategorySerializer(data=request.data)
            if category_serializer.is_valid(raise_exception=False):
                category_serializer.save()
                self.response['status'] = True
                self.response['category'] = category_serializer.data
            else:
                self.response['error'] = category_serializer.errors
        except Exception as e:
            self.response['error'] = f'{e.__class__.__name__}'
        return Response(self.response)

    def delete(self, request):
        try:
            category = Category.objects.get(name=request.data['name'])
            self.response['message'] = f"{category} successfully deleted"
            category.delete()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class TagsList(APIView):
    permission_classes = [IsRestaurantOrReadOnly]
    response = {
        'status': False
    }

    def get(self, request):
        try:
            tags = Tags.objects.all()
            tags_serializer = TagsSerializer(tags, many=True)
            self.response['tag'] = tags_serializer.data
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f'{e.__class__.__name__}'
        return Response(self.response)

    def post(self, request):
        try:
            tags_serializer = TagsSerializer(data=request.data)
            if tags_serializer.is_valid(raise_exception=False):
                tags_serializer.save()
                self.response['status'] = True
                self.response['tag'] = tags_serializer.data
            else:
                self.response['error'] = tags_serializer.errors
        except Exception as e:
            self.response['error'] = f'{e.__class__.__name__}'
        return Response(self.response)

    def delete(self, request):
        try:
            tag = Tags.objects.get(name=request.data['name'])
            self.response['message'] = f"{tag} successfully deleted"
            tag.delete()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class FoodItemsList(APIView):
    permission_classes = [IsRestaurantOrReadOnly]
    response = {
        'status': False
    }

    def get(self, request):
        data = request.data
        user = request.user
        try:
            if user.is_anonymous or user.is_customer:
                food_items = FoodItems.objects.filter(is_available=True)
            else:
                food_items = FoodItems.objects.filter()
            if data.get('name'):
                food_items = food_items.filter(name__icontains=data['name'])
            if data.get('category'):
                food_items = food_items.filter(category__name=data['category'])
            if data.get('tags'):
                food_items = food_items.filter(tags__name=data['tags'])
            if data.get('price'):
                #  max price and min price must be specified if search by price
                max_price = data['price']['max_price']
                min_price = data['price']['min_price']
                food_items = food_items.filter(
                    Q(price__gte=min_price) & Q(price__lte=max_price))
            if data.get('restaurant'):
                restaurants = Restaurant.objects.filter(
                    name__icontains=data['restaurant'])
                food_items = get_food_items(restaurants)
            if data.get('discount'):
                discounted_food_items = Discount.objects.filter()
                food_items = [item.food_item for item in discounted_food_items]
                print(food_items)
            self.response['food_items'] = food_items_details(food_items)
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)

    def post(self, request):
        # {
        #     "category": 1,
        #     "tags": [1,2,3,60],
        #     "image": ,
        #     "name": "postmane",
        #     "price": 500,
        #     "is_available": true
        # }
        data = request.data
        user = request.user
        try:
            category = Category.objects.get(id=data['category'])
            food_item = FoodItems.objects.create(
                restaurant=user.restaurant,
                category=category,
                name=data['name'],
                image=data.get('image'),
                price=data['price'],
            )
            add_tags_to_food_item(food_item, data['tags'])
            self.response['food_item'] = food_items_details([food_item])
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class FoodItemDetail(APIView):
    permission_classes = [IsRestaurantOrReadOnly]
    response = {
        'status': False
    }

    def get(self, request, pk):
        try:
            food_item = FoodItems.objects.get(id=pk)
            self.response['food_item'] = food_items_details([food_item])
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)

    @restaurant_owner_only
    def put(self, request, pk):
        data = request.data
        try:
            food_item = FoodItems.objects.get(id=pk)
            if data.get('category'):
                category = Category.objects.get(id=data['category'])
                food_item.category = category
            if data.get('name'):
                food_item.name = data['name']
            if data.get('image'):
                food_item.image = data['image']
            if data.get('price'):
                food_item.price = data['price']
            if data.get('is_available'):
                food_item.is_available = data['is_available']
            if data.get('tags'):
                # {
                #     ...
                #     "tags": None / {
                #         "add_tags": None / [__ids__],
                #         "remove_tags": None / [__ids__]
                #         }
                # }
                if data['tags'].get('add_tags'):
                    add_tags_to_food_item(food_item, data['tags']['add_tags'])
                if data['tags'].get('remove_tags'):
                    for tag in data['tags']['remove_tags']:
                        tag_obj = Tags.objects.filter(id=tag)
                        if tag_obj.exists():
                            food_item.tags.remove(tag_obj[0])
            food_item.save()
            self.response['food_item'] = food_items_details([food_item])
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e}"
        return Response(self.response)

    @restaurant_owner_only
    def delete(self, request, pk):
        try:
            food_item = FoodItems.objects.get(id=pk)
            food_item_name = food_item.name
            food_item.delete()
            self.response['status'] = True
            self.response['message'] = f"{food_item_name} successsfully deleted."
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class DiscountView(APIView):

    permission_classes = [IsRestaurantOrReadOnly]
    response = {
        'status': False
    }

    @restaurant_owner_only
    def post(self, request):
        # {
        #     "food_item_id": 32,
        #     "discount": {
        #         "discount_type": "percentage",
        #         "discount_amount": 10.12
        #     }
        # }
        data = request.data
        try:
            food_item = FoodItems.objects.get(id=data['food_item_id'])
            discount = Discount.objects.create(
                discount_type=data['discount']['discount_type'],
                discount_amount=data['discount']['discount_amount'],
                food_item=food_item
            )
            food_item_name = food_item.name
            self.response['message'] = f"Discount for {food_item_name}created successfully."
            self.response['status'] = True
        except Exception as e:
            self.response['error'] ={
                f"{e.__class__.__name__}": e 
            } 
        return Response(self.response)

    @restaurant_owner_only
    def put(self, request):
        data = request.data
        try:
            discount = Discount.objects.get(food_item__id=data['food_item_id'])
            if data.get('discount_type'):
                discount.discount_type = data['discount_type']
            if data.get('amount'):
                discount.discount_amount = data['discount_amount']
            discount.save()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = {
                f"{e.__class__.__name__}": e
            }
        return Response(self.response)

    @restaurant_owner_only
    def delete(self, request):
        data = request.data
        try:
            discount = Discount.objects.get(food_item__id=data['food_item_id'])
            discount.delete()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)
