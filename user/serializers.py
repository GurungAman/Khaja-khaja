from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Customer, CustomUser
from auth_operations.utils import password_validator

User = get_user_model()


class CreateBaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,)
    password_1 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'primary_phone_number',
                  'password', 'password_1')

    def save(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            primary_phone_number=validated_data['primary_phone_number']
        )
        password1 = validated_data['password']
        password2 = validated_data['password_1']

        if password_validator(password1, password2):
            user.set_password(password1)
            user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    base_user = CreateBaseUserSerializer(source='customer')

    class Meta:
        model = Customer
        fields = ('base_user', 'id', 'first_name',
                  'middle_name', 'last_name', 'address')

    def save(self, validated_data):
        base_user = dict(validated_data.pop('base_user'))
        user = User.objects.get(email=base_user['email'])
        customer = Customer.objects.create(
            customer=user,
            first_name=validated_data['first_name'],
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data['last_name'],
            address=validated_data['address'],
        )
        return customer


class UpdateCustomerSerializer(serializers.ModelSerializer):
    primary_phone_number = serializers.CharField(max_length=10, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Customer
        fields = ('primary_phone_number', 'first_name',
                  'middle_name', 'last_name', 'address', )

    def update(self, instance, validated_data, **kwargs):
        if validated_data.get("primary_phone_number"):
            base_user = kwargs.get("base_user")
            base_user.primary_phone_number = validated_data['primary_phone_number']
            base_user.save()
        if validated_data.get("first_name"):
            instance.first_name = validated_data['first_name']
        if validated_data.get("middle_name"):
            instance.middle_name = validated_data['middle_name']
        if validated_data.get("last_name"):
            instance.last_name = validated_data['last_name']
        if validated_data.get("address"):
            instance.address = validated_data['address']
        instance.save()
