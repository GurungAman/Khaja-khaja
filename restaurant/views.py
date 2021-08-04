from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Category, Tags, Menu, FoodItems, Restaurant
from .serializers import CategorySerializer, TagsSerializer, MenuSerializer, FoodItemsSerializer, RestaurantSerializer
from .restaurant_utils import  menu_details, food_items_details, get_food_items

from permissions import RestaurantOnly

# Create your views here.

class CategoryList(APIView):
    # create, delete category and get all categories
    permission_classes = [IsAuthenticated, RestaurantOnly]
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
            self.response['status'] = False
            self.response['message'] = {
                'error': f'{e.__class__.__name__}'
            }
        response = (self.response)
        return Response(response)
    
    def post(self, request):
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            self.response['status'] = True
            self.response['category'] = category_serializer.data
        else:
            self.response['status'] = False
            self.response['error'] = category_serializer.errors
        return Response(self.response)

    def delete(self, request):
        try:
            category = Category.objects.get(name = request.data['name'])
            self.response['message'] = f"{category} successfully deleted"
            category.delete()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
            self.response['status'] = False
        return Response(self.response)


class TagsList(APIView):
    permission_classes = [IsAuthenticated, RestaurantOnly]
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
            self.response['message'] = {
                'error': f'{e.__class__.__name__}'
            }
        response = (self.response)
        return Response(response)

    def post(self, request):
        tags_serializer = TagsSerializer(data=request.data)
        if tags_serializer.is_valid():
            tags_serializer.save()
            self.response['status'] = True
            self.response['tag'] = tags_serializer.data
        else:
            self.response['error'] = tags_serializer.errors
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


class MenuList(APIView):
    permission_classes = [IsAuthenticated, RestaurantOnly]
    response = {
        'status': False
    }

    def get(self, request):
        try:
            menu = Menu.objects.all()
            self.response['menu'] = menu_details(menu)
            self.response['status'] = True
        except Exception as e:
            self.response['message'] = {
                'error': f'{e.__class__.__name__}'
            }
        response = (self.response)
        return Response(response)

    def post(self, request):
        data = request.data
        try:
            menu = Menu.objects.create(
                restaurant = request.user.restaurant,
                name = data['name'],
                is_active = data['is_active']
            )
            self.response['menu'] = MenuSerializer(menu).data
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)

    def put(self, request):
        data = request.data
        try:
            menu = Menu.objects.get(restaurant = request.user.restaurant, name=request.data['name'])
            if data.get('name'):
                menu.name = data['name']
            if data.get('is_active'):
                menu.is_active = data['is_active']
            menu.save()
            self.response['message'] = f"{menu} successfully Updated"
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)
        
    def delete(self, request):
        try:
            menu = Menu.objects.get(restaurant = request.user.restaurant, name=request.data['name'])
            self.response['message'] = f"{menu} successfully deleted"
            menu.delete()
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)


class FoodItemsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, RestaurantOnly]
    response = {
        'status': False
    }

    def get(self, request):
        data = request.data
        try:
            food_items = FoodItems.objects.filter()
            if data.get('name'):
                food_items = food_items.filter(name__icontains=data['name'])
            if data.get('category'):
                food_items = food_items.filter(category__name = data['category'])
            if data.get('tags'):
                food_items = food_items.filter(tags__name=data['tags'])
            if data.get('price'):
                max_price = data['price'].get('max_price')
                min_price = data['price'].get('min_price')
                food_items = food_items.filter(Q(price__gte = min_price) & Q(price__lte = max_price))
            if data.get('restaurant'):
                restaurants = Restaurant.objects.filter(name__icontains = data['restaurant'])
                food_items = get_food_items(restaurants)
            self.response['food_items'] = food_items_details(food_items)
            self.response['status'] = True
        except Exception as e:
            self.response['error'] = f"{e.__class__.__name__}"
        return Response(self.response)
        

