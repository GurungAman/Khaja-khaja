from django.db import models
from user.models import Customer
from restaurant.models import FoodItems

# Create your models here.

class OrderItem(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.user.first_name} {self.food_item.name}"
    
    def save(self, *args, **kwargs):
        self.cost = self.food_item.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)


class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered')
    )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    order_status = models.CharField(max_length=50, choices=STATUS, default='pending')
    shipping_address = models.CharField(max_length=100)
    discount_price = models.PositiveIntegerField(blank=True, default=0)
    total_cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_name
