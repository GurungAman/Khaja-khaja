from django.db import models
from user.models import Customer
from restaurant.models import FoodItems

# Create your models here.


class OrderItem(models.Model):
    user = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_order_item")
    food_item = models.ForeignKey(
        FoodItems, on_delete=models.CASCADE, related_name="food_item")
    quantity = models.PositiveIntegerField(default=1)
    cost = models.PositiveIntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.food_item.name}"

    def save(self, *args, **kwargs):
        self.cost = self.food_item.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)


class Order(models.Model):
    STATUS = (
        ('order_created', 'Order Created'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered')
    )
    user = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_order")
    order_items = models.ManyToManyField(OrderItem)
    order_status = models.CharField(
        max_length=50, choices=STATUS, blank=True, null=True)
    shipping_address = models.CharField(max_length=100, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_name
