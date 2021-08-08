from django.contrib.auth import  get_user_model
from rest_framework import serializers
from .models import Category, Tags, Menu, FoodItems, Restaurant
from user.serializers import CreateBaseUserSerializer

User = get_user_model()

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
    base_user = CreateBaseUserSerializer(source='restaurant')

    class Meta:
        model = Restaurant
        fields = ('base_user', 'id', 'name', 'logo',
                  'license_number', 'seconday_phone_number', 'address', 'bio')

    def save(self, validated_data):
        base_user = dict(validated_data.pop('base_user'))
        user = User.objects.get(email = base_user['email'])
        restaurant = Restaurant.objects.create(
            restaurant = user,
            name = validated_data['name'],
            logo = validated_data.get('logo'),
            license_number = validated_data['license_number'],
            address = validated_data['address'],
            seconday_phone_number = validated_data.get('seconday_phone_number'),
            bio = validated_data.get('bio'),
        )
        return restaurant


class UpdateRestaurantSerializer(serializers.ModelSerializer):
    primary_phone_number = serializers.CharField(max_length=50, required=False)
    license_number = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Restaurant
        fields = ('primary_phone_number', 'name', 'logo', 'license_number', 'seconday_phone_number', 'address', 'bio')
