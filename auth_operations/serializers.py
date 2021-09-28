from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    force_str, smart_bytes)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from .utils import password_validator
from tasks import send_mail_task


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


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def email_validate(self, validated_data):
        email = validated_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id_b64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            domain = validated_data.get('domain')
            relative_link = reverse(
                'password_reset_token',
                kwargs={"uidb64": user_id_b64, "token": token})
            absolute_url = "http://" + domain + relative_link
            subject = "Reset Password."
            message = "H! \n Please click on the link below to" \
                f"reset your password.\n {absolute_url}"
            recipient_list = [user.email]
            send_mail_task.delay(subject, message, recipient_list)
        else:
            raise ObjectDoesNotExist("Invalid email.")


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)
    user_id_b64 = serializers.CharField(required=True, write_only=True)

    def validate(self, validated_data):
        try:
            token = validated_data.get('token')
            user_id_b64 = validated_data.get('user_id_b64')

            user_id = force_str(urlsafe_base64_decode(user_id_b64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Invalid URL.')

            password1 = validated_data['password']
            password2 = validated_data['password1']
            if password_validator(password1, password2):
                print("validated")
                user.set_password(password1)
                user.save()
        except Exception as e:
            raise Exception(e)
        return super().validate(validated_data)
