from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_delete, pre_save
from django.dispatch import receiver
from .models import Order, Discount


@receiver(m2m_changed, sender=Order.order_items.through)
def update_total_cost(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        cost = 0
        order_items = instance.order_items.all()
        for order_item in order_items:
            cost += order_item.cost
        instance.total_cost = cost
        instance.save()


@receiver(pre_save, sender=Discount)
def update_total_cost_with_discount(sender, instance, **kwargs):
    order = instance.order
    order_total_cost = order.total_cost
    if instance.discount_type == 'amount':
        order_total_cost -= instance.discount
    else:
        discount_amount = order_total_cost / instance.discount
        order_total_cost -= discount_amount
    if order_total_cost <= 0:
        raise ValidationError("Disocunt shouldn't be greater than total cost.")
    order.total_cost = order_total_cost
    order.save()


@receiver(pre_delete, sender=Order)
def delete_order_items(sender, instance, **kwargs):
    for order_item in instance.order_items.all():
        order_item.delete()
