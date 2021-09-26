from functools import wraps
from rest_framework.response import Response
from .models import FoodItems


def restaurant_owner_only(func):
    @wraps(func)
    def wrapper_function(self, request, pk=None, *args, **kwargs):
        user = request.user.restaurant
        response = {'status': False, }
        try:
            if pk:
                food_item = FoodItems.objects.get(id=pk)
                if not user == food_item.restaurant:
                    response['error'] = "You are not "\
                        "authorized to make changes to this item."
                    return Response(response)
                return func(self, request, pk, *args, **kwargs)
            else:
                data = request.data
                food_item = FoodItems.objects.get(id=data['food_item_id'])
                if not user == food_item.restaurant:
                    response['error'] = "Permission denied."
                    return Response(response)
                return func(self, request, *args, **kwargs)
        except Exception as e:
            response['error'] = f'{e.__class__.__name__}'
            return Response(response)
    return wrapper_function
