from datetime import timedelta
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from celery.utils.log import get_task_logger
from decouple import config

from khaja_khaja.celery import app
from cart.models import Order
from notification.models import Notification


logger = get_task_logger(__name__)
User = get_user_model()


@app.task(bind=True, max_retries=3)
def send_mail_task(self, subject, message, recipient_list):
    from_email = config("FROM_EMAIL")
    send_mail(subject, message, from_email, recipient_list)
    return None


# @shared_task
@app.task(bind=True, max_retries=3)
def create_notification(self, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.order_items.all()
    for order_item in order_items:
        restaurant = order_item.food_item.restaurant
        Notification.objects.create(
            user=restaurant,
            order_item=order_item,
            shipping_address=order.shipping_address,
        )
        order_item.ordered = True
        order_item.save()
    order.order_status = 'order_created'
    order.save()
    return None


@app.task(bind=True, max_retries=3)
def send_verify_users_email(self, user_id, **kwargs):
    user = User.objects.get(id=user_id)
    access_token = AccessToken.for_user(user)
    access_token.set_exp(lifetime=timedelta(minutes=10))
    domain = kwargs.get('domain')
    relative_link = reverse('verify_email')
    absolute_url = "http://" + domain + \
        relative_link + "?token=" + str(access_token)
    subject = "Verify email."
    message = "HI! \n Please click on the link below to" \
        f"verify your email address.\n {absolute_url}"
    # URL will be invalid after 10 minutes
    recipient_list = [user.email]
    send_mail_task(subject, message, recipient_list)
    return None
