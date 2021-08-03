from rest_framework.permissions import BasePermission

class RestaurantOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_restaurant:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_restaurant:
            return True
        return False
