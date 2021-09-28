from django.contrib.auth import get_user_model
from rest_framework import serializers
from .utils import password_validator


User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def update(self, *args, **kwargs):
        user = kwargs.pop('user')
        validated_data = kwargs

        if not user.check_password(validated_data['old_password']):
            raise serializers.ValidationError({
                "Password": "Wrong Password."
            })

        password1 = validated_data['new_password']
        password2 = validated_data['new_password1']
        if password_validator(password1, password2):
            print("validated")
            user.set_password(password1)
            user.save()
        return user
