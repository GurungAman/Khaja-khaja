from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.user_manager import UserManager
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.

# Custom Base user
# Will be used to extend user models to restaurant and customers
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    primary_phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)

    # admin privileges
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    is_customer = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Customer(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        customer = self.customer
        # customer is inactive and can only use app after verifying through mail
        # will be added later
        # customer.is_active = False
        customer.is_customer = True
        customer.is_restaurant = False
        customer.save()
        super(Customer, self).save(*args, **kwargs)
