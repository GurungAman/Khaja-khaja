from .serializers import MenuSerializer, FoodItemsSerializer, TagsSerializer, RestaurantSerializer
from .models import FoodItems, Menu, Category, Tags

def restaurant_details(restaurants):
    response  = []
    for restaurant in restaurants:
        restaurant_serializer = RestaurantSerializer(restaurant)
        data = restaurant_serializer.data
        base_user = data.pop('base_user')
        data['email'] = base_user['email']
        data['primary_phone_number'] = base_user['primary_phone_number']
        response.append(data)
    return response


def menu_details(menu):
    response = []
    for item in menu:
        menu_serializer= MenuSerializer(item)
        data = menu_serializer.data
        data['total_items'] = item.menu.all().count()
        response.append(data)
    return response


def get_tags(tags):
    response = []
    for tag in tags:
        tag_name = Tags.objects.get(id = tag).name
        response.append(tag_name)
    return response


def food_items_details(food_items):
    response = []
    for item in food_items:
        food_items_serializer = FoodItemsSerializer(item)
        data = food_items_serializer.data
        menu = Menu.objects.get(id = data['menu'])
        data['menu'] = menu.name
        data['restaurant'] = menu.restaurant.name
        data['category'] = Category.objects.get(id = data['category']).name
        data['tags'] = get_tags(tags = data['tags'])
        response.append(data)
    return response 

def get_food_items(restaurants):
    food_items = []
    for restaurant in restaurants:
        food_item = FoodItems.objects.filter(menu__restaurant = restaurant)    
        for x in food_item:
            food_items.append(x)
    return food_items
