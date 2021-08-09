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
        return self.user.get_name
    
    def save(self, *args, **kwargs):
        self.cost = self.food_item.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    total_cost = models.PositiveIntegerField(default=0)
    shipping_addrses = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_name
    
    @property
    def get_total_cost(self):
        cost = 0
        for order_item in self.order_items.all():
            cost += order_item.cost
        return cost

    def save(self, *args, **kwargs):
        self.total_cost = self.get_total_cost
        super(Order, self).save(*args, **kwargs)
