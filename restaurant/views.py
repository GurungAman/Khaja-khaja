import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Category, Tags, Menu, FoodItems, Restaurant
from .serializers import CategorySerializer
from utils import JWT_get_user

# Create your views here.

class CategoryList(APIView):
    # create category and get all categories
    permissions = [IsAuthenticated]
    response = {
        'status': False
        }
    
    def get(self, request):
        user = JWT_get_user(request=request)
        if user is not None:        
            try:
                categories = Category.objects.all()
                category_serializer = CategorySerializer(categories, many=True)
                self.response['category'] = category_serializer.data
                print(type(category_serializer.data))
                self.response['status'] = True
            except Exception as e:
                self.response['message'] = {
                    'error': f'{e.__class__.__name__}'
                }
        
        response = (self.response)
        return Response(response)
    
    def post(self, request):
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
        self.response['status'] = True
        self.response['category'] = category_serializer.data
        return Response(self.response)






