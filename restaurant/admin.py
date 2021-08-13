from django.contrib import admin
from .models import Restaurant, Category, Tags, FoodItems, Menu, Discount


# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(FoodItems)
admin.site.register(Menu)
admin.site.register(Discount)
