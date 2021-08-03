from django.db import models
from django.conf import settings

# Create your models here.

class Restaurant(models.Model):
    restaurant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurant/logo/', blank=True)
    license_number = models.CharField(max_length=50)
    seconday_phone_number = models.CharField(blank=True, max_length=50)
    address = models.CharField(max_length=100)
    bio = models.TextField(blank=True, max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        restaurant = self.restaurant
        restaurant.is_customer = False
        restaurant.is_restaurant = True
        super(Restaurant, self).save(*args, **kwargs)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_menu')
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.restaurant.name}"
    
    class  Meta:
        unique_together = ['restaurant', 'name']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class FoodItems(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='menu')
    category = models.ForeignKey(
        Category, related_name='category', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tags, related_name='tags', blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurant/food/', blank=True)
    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['menu', 'name',]
