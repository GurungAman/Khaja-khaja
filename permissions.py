from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRestaurantOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        #  called on all http request
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return False
        return request.user.is_restaurant


class IsCustomerOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_customer


class IsRestaurantOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_restaurant
