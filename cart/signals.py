from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.dispatch import receiver
from .models import Order
from notification.models import Notification


@receiver(m2m_changed, sender=Order.order_items.through)
def update_total_cost(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        cost = 0
        order_items = instance.order_items.all()
        for order_item in order_items:
            cost += order_item.cost
        instance.total_cost = cost
        instance.save()


@receiver(pre_delete, sender=Order)
def delete_order_items(sender, instance, **kwargs):
    for order_item in instance.order_items.all():
        order_item.delete()


# @receiver(post_save, sender=Order)
# def update_order_items_status(sender, instance, **kwargs):
#     for order_item in instance.order_items.all():
#         order_item.ordered = True
#         order_item.save()
