from functools import wraps
from rest_framework.response import Response
from .models import FoodItems

def restaurant_owner_only(func):
    @wraps(func)
    def wrapper_function(self, request, *args, **kwargs):
        user = request.user
        response = {'status': False,}
        try:
            food_item = FoodItems.objects.get(id=kwargs['pk'])
            if not user == food_item.menu.restaurant.restaurant:
                response['error'] = "Permission denied."
                return Response(response)
        except Exception as e:
            response['error'] = f'{e.__class__.__name__}'
            return Response(response)
        return func(self, request, *args, **kwargs)
    return wrapper_function
