from django.db import models
from django.conf import settings
from user.models import CustomUser
# Create your models here.


class Restaurant(models.Model):
    restaurant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name='restaurant')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurant/logo/', blank=True)
    license_number = models.CharField(max_length=50)
    seconday_phone_number = models.CharField(blank=True, max_length=50)
    # address = models.CharField(max_length=100)
    # bio = models.TextField(blank=True, max_length=200)
    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        restaurant = self.restaurant
        restaurant.is_customer = False
        restaurant.is_restaurant = True
        super(Restaurant, self).save(*args, **kwargs)
