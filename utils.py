from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def get_access_token(data):
    # Only active users can get access token
    token_pair = TokenObtainPairSerializer().validate(data)
    access_token = token_pair['access']
    return access_token
