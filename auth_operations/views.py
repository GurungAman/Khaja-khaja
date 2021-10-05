from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str)
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
import jwt
from .serializers import (
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer
)


User = get_user_model()

# Create your views here.


@extend_schema(request=ChangePasswordSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = request.data
    response = {'status': False}
    try:
        password_serializer = ChangePasswordSerializer(data=data)
        if password_serializer.is_valid(raise_exception=False):
            password_serializer.update(user=user, **data)
            response['status'] = True
            response['message'] = "Password updated successfully."
        else:
            response['error'] = password_serializer.errors
    except Exception as e:
        # print((e.args[0]))
        response['error'] = {f"{e.__class__.__name__}": f"{e}"}
    return Response(response)


@extend_schema(request=ResetPasswordSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_request(request):
    data = request.data
    response = {"status": False}
    try:
        current_site = get_current_site(request)
        data['domain'] = current_site.domain
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.email_validate(validated_data=data)
            response['status'] = True
            response['message'] = "We have sent you a " \
                "link to reset your password."
    except Exception as e:
        response['error'] = {f"{e.__class__.__name__}": f"{e}"}
    return Response(response)


@api_view(['GET'])
def check_password_token(request, uidb64, token):
    response = {"status": False}
    try:
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            response['message'] = "Invalid URL. Please try again."
        else:
            response['status'] = True
            response['message'] = "Valid credentials"
            response['user_id'] = uidb64
            response['token'] = token
    except Exception as e:
        response['error'] = {f"{e.__class__.__name__}": f"{e}"}
    return Response(response)


@extend_schema(request=SetNewPasswordSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def set_new_password(request):
    response = {"status": False}
    try:
        data = request.data
        serializer = SetNewPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            response['status'] = True
            response['message'] = "Password Reset successful."
    except Exception as e:
        response['error'] = {f"{e.__class__.__name__}": f"{e}"}
    return Response(response)


@api_view(['GET'])
def verify_email(request):
    response = {'status': True}
    token = request.GET.get('token')
    secret_key = settings.SECRET_KEY
    algorithm = settings.SIMPLE_JWT['ALGORITHM']
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user = User.objects.get(id=payload['user_id'])
        if not user.is_active:
            user.is_active = True
            user.save()
            response['message'] = "Email successfully verified."
        else:
            response['message'] = "Email already verified. "
        response['status'] = True
    except Exception as e:
        response['error'] = {f"{e.__class__.__name__}": f"{e}"}
    return Response(response)
