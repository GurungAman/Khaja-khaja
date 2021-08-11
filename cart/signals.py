from django.db.models.signals import m2m_changed, post_save, pre_delete, pre_save

from django.dispatch import receiver
from .models import Order

@receiver(m2m_changed, sender=Order.order_items.through)
def update_total_cost(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        cost = 0
        order_items = instance.order_items.all()
        for order_item in order_items:
            cost += order_item.cost
        if instance.discount_price > 0 and cost > 0:
            cost -= instance.discount_price
        instance.total_cost = cost
        instance.save()

@receiver(pre_delete, sender=Order)
def delete_order_items(sender, instance, **kwargs):
    for order_item in instance.order_items.all():
        order_item.delete()
