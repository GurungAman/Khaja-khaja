from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(pre_delete, sender=OrderItem)
@receiver(m2m_changed, sender=Order.order_items.through)
def update_total_cost(sender, **kwargs):
    instance = kwargs.get('instance')
    action = kwargs.get("action")
    if sender.__name__ == "OrderItem":
        user = instance.user
        order = Order.objects.get(user=user, order_status=None)
        order.total_cost -= instance.cost
        order.save()
    elif action == 'post_add' or action == 'post_remove':
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


@receiver(post_save, sender=OrderItem)
def create_order(sender, instance, **kwargs):
    customer = instance.user
    order, _ = Order.objects.get_or_create(user=customer, order_status=None)
    order.order_items.add(instance)
    order.save()
