from django.db import models
from restaurant.models import Restaurant
from cart.models import OrderItem

# Create your models here.


class Notification(models.Model):
    NOTI_STATUS = (
        ("R", "Read"),
        ("U", "Unread")
    )
    user = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=NOTI_STATUS, default="U")
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.order_item.food_item.name
