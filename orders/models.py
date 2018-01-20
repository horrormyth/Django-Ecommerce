from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
from carts.models import Cart


class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.email


ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=123)

    def __unicode__(self):
        return '{}, {}'.format(self.street, self.city)

    def get_address(self):
        return '{}, {}, {},{}'.format(self.street, self.city, self.state, self.zipcode)


class Order(models.Model):
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout, null=True)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True)
    shipping_total_price = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        default=5.99
    )
    order_total = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        default=5.99)

    def __unicode__(self):
        return '{}'.format(self.cart.id)


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total
