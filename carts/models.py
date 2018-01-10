from django.conf import settings
from django.db import models

# Create your models here.
from products.models import Variation


class CartItem(models.Model):
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return self.item.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.id)
