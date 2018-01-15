from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from products.models import Variation


class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=20)

    def __unicode__(self):
        return str(self.id)

    def update_subtotal(self):
        subtotal = 0
        for item in self.cartitem_set.all():
            subtotal += item.line_item_total

        self.subtotal = subtotal
        self.save()


@receiver(pre_save, sender=CartItem)
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    """ Pre-save the line item total after calculating the amount and the price """
    quantity = instance.quantity
    if quantity >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(quantity) * Decimal(price)
        instance.line_item_total = line_item_total


@receiver(post_delete, sender=CartItem)
@receiver(post_save, sender=CartItem)
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    """Save the subtotal to Cart after calcualting the total of each items in the """
    instance.cart.update_subtotal()


