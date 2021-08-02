from rest_framework import serializers
from .models import Category, Tags, Menu, FoodItems, Restaurant

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
         model = Category
         fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
     class Meta:
         model = Tags
         fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
     class Meta:
         model = Menu
         fields = '__all__'


class FoodItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
