from django.core.mail import send_mail
from celery import Celery
from decouple import config
from cart.models import Order
from .models import Notification


app = Celery()


@app.task
def send_mail_task(subject, message, recipient_list):
    from_email = config('FROM_EMAIL')
    send_mail(subject, message, from_email, recipient_list)
    return None


# @shared_task
@app.task
def create_notification(order):
    order = Order.objects.get(order=order)
    order_items = order.order_items.all()
    for order_item in order_items:
        restaurant = order_item.food_item.restaurant
        Notification.objects.create(
            user=restaurant,
            order_item=order_item
        )
    return None
