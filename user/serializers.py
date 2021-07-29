from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Customer, CustomUser

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True,)
    password_1 = serializers.CharField(write_only=True, required = True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'primary_phone_number', 'password', 'password_1')


    def save(self):

        user = CustomUser(
            email = self.validated_data['email'],
            primary_phone_number = self.validated_data['primary_phone_number']
            )
        password1 = self.validated_data['password']
        password2 = self.validated_data['password_1']

        if password1 != password2 or password1 is None:
            raise serializers.ValidationError({"Password": "Password must match."})
        user.set_password(password1)
        user.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(source='customer')

    class Meta:
        model = Customer
        fields = ('custom_user', 'id', 'first_name', 'middle_name', 'last_name', 'address' )

    def save(self, validated_data):
        custom_user = dict(validated_data.pop('custom_user'))
        user = User.objects.get(email=custom_user['email'])
        customer, created = Customer.objects.update_or_create(
            customer = user,
            first_name = validated_data['first_name'],
            middle_name = validated_data['middle_name'],
            last_name = validated_data['last_name'],
            address = validated_data['address'], 
            )
        return customer