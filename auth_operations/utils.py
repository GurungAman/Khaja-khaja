from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


def password_validator(password1, password2):
    if password1 != password2:
        raise serializers.ValidationError({
            "Password": "Password must match."
        }
        )
    try:
        validate_password(password1)
    except Exception as e:
        raise ValidationError(e)
    return True
