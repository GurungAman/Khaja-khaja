from django.contrib import admin
from django.contrib.auth.models import Group
from user.models import CustomUser
from user.custom_user_admin import CustomUserAdmin

# Register your models here
admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
