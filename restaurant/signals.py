from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Discount

@receiver(pre_save, sender=Discount)
def update_food_item_price(sender, instance, **kwargs):
    food_item = instance.food_item
    food_item_price = food_item.price
    print(instance.discount_amount)
    if instance.discount_type == 'amount':
        food_item_price -= instance.discount_amount
    else:
        discounted_price = (food_item_price * instance.discount_amount) / 100
        food_item_price -= discounted_price
    if food_item_price <= 0:
        raise ValidationError("Disocunt shouldn't be greater than total cost.")
    food_item.price = food_item_price
    food_item.save()
    

@receiver(pre_delete, sender=Discount)
def reset_food_item_price(sender, instance, **kwargs):
    food_item = instance.food_item
    food_item_price = food_item.price
    if instance.discount_type == 'amount':
        food_item_price += instance.discount_amount
    else:
        food_item_price /= 1 - (instance.discount_amount / 100)
    food_item.price = food_item_price
    food_item.save()
