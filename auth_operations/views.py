from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt
from .serializers import (
    ChangePasswordSerializer
)


User = get_user_model()

# Create your views here.


@api_view(['POST'])
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
