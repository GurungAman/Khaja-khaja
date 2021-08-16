from django.contrib.auth import  get_user_model
from rest_framework import serializers
from .models import Category, Tags, FoodItems, Restaurant
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

class FoodItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    base_user = CreateBaseUserSerializer(source='restaurant')

    class Meta:
        model = Restaurant
        fields = ('base_user', 'id', 'name', 'logo',
                  'license_number', 'secondary_phone_number', 'address', 'bio')

    def save(self, validated_data):
        base_user = dict(validated_data.pop('base_user'))
        user = User.objects.get(email = base_user['email'])
        restaurant = Restaurant.objects.create(
            restaurant = user,
            name = validated_data['name'],
            logo = validated_data.get('logo'),
            license_number = validated_data['license_number'],
            address = validated_data['address'],
            secondary_phone_number = validated_data.get('secondary_phone_number'),
            bio = validated_data.get('bio'),
        )
        return restaurant


class UpdateRestaurantSerializer(serializers.ModelSerializer):
    license_number = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Restaurant
        fields = ('name', 'logo', 'license_number', 'secondary_phone_number', 'address', 'bio')

    def update(self, instance, validated_data):
        if validated_data.get('name'):
            instance.name = validated_data['name']
        if validated_data.get('logo'):
            instance.logo = validated_data['logo']
        if validated_data.get('license_number'):
            instance.license_number = validated_data['license_number']
        if validated_data.get('secondary_phone_number'):
            instance.secondary_phone_number = validated_data['secondary_phone_number']
        if validated_data.get('address'):
            instance.address = validated_data['address']
        if validated_data.get('bio'):
            instance.bio = validated_data['bio']
        instance.save()
        return instance
