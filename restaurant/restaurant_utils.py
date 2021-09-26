from .serializers import FoodItemsSerializer, RestaurantSerializer
from .models import Discount, FoodItems, Restaurant, Category, Tags


def restaurant_details(restaurants):
    # takes queryset as parameter
    response = []
    for restaurant in restaurants:
        restaurant_serializer = RestaurantSerializer(restaurant)
        data = restaurant_serializer.data
        base_user = data.pop('base_user')
        data['email'] = base_user['email']
        data['primary_phone_number'] = base_user['primary_phone_number']
        response.append(data)
    return response


def get_tags(tags):
    response = []
    for tag in tags:
        tag_name = Tags.objects.get(id=tag).name
        response.append(tag_name)
    return response


def food_items_details(food_items):
    response = []
    for item in food_items:
        food_items_serializer = FoodItemsSerializer(item)
        data = food_items_serializer.data
        restaurant = Restaurant.objects.get(id=data['restaurant'])
        data['restaurant'] = restaurant.name
        data['category'] = Category.objects.get(id=data['category']).name
        data['tags'] = get_tags(tags=data['tags'])
        discount = Discount.objects.filter(food_item__id=data['id'])
        if discount.exists():
            data['discount'] = discount[0].discount_amount
        else:
            data['discount'] = 0
        data.pop('is_available')
        response.append(data)
    return response


def get_food_items(restaurants):
    food_items = []
    for restaurant in restaurants:
        food_item = FoodItems.objects.filter(
            restaurant=restaurant, is_available=True)
        for x in food_item:
            food_items.append(x)
    return food_items


def add_tags_to_food_item(food_item, tags):
    # takes instance of food_item and a list of ids of tags
    for tag in tags:
        tag_obj = Tags.objects.get(id=tag)
        food_item.tags.add(tag_obj)
        # if tag_obj.exists():
        #     food_item.tags.add(tag_obj[0])
