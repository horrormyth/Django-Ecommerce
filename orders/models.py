from decimal import Decimal

import braintree
from braintree.exceptions.authentication_error import AuthenticationError
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.
from carts.models import Cart

# TODO  Put the constants separately and log if not authenticated properly

BRAINTREE_PUBLIC_KEY = getattr(settings, 'BRAINTREE_PUBLIC_KEY', None)
BRAINTREE_PRIVATE_KEY = getattr(settings, 'BRAINTREE_PRIVATE_KEY', None)
BRAINTREE_MERCHANT_ID = getattr(settings, 'BRAINTREE_MERCHANT_ID', None)

try:
    braintree.Configuration.configure(environment='sandbox',
                                      merchant_id=BRAINTREE_MERCHANT_ID,
                                      public_key=BRAINTREE_PUBLIC_KEY,
                                      private_key=BRAINTREE_PRIVATE_KEY
                                      )
    braintree_authentciated = True
except AuthenticationError as error:
    braintree_authentciated = False


class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return self.email

    @property
    def get_braintree_id(self):
        if braintree_authentciated:
            result = braintree.Customer.create({
                "email": self.email,
            }
            )
            if result.is_success:
                self.braintree_id = result.customer.id
                self.save()

        return self.braintree_id


    def get_braintree_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                'customer_id': customer_id
            })
            return client_token
        return None


@receiver(post_save, sender=UserCheckout)
def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id


# TODO add error handling.


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


ORDER_STATUS = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
)


class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS, default='created')
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
    transaction_id = models.CharField(max_length=25, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.cart.id)

    def mark_completed(self):
        self.status = 'paid'
        self.save()


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total
