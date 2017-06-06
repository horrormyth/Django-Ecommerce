from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class ProdutQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProdutQuerySet(self.model, using = self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length = 512)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places = 2, max_digits = 20 )
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs = {'pk': self.pk})


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length = 512)
    price = models.DecimalField(decimal_places = 2, max_digits = 20)
    sale_price = models.DecimalField(decimal_places = 2, max_digits = 20, null = True, blank = True)
    active = models.BooleanField(default = True)
    inventory = models.IntegerField(null = True, blank = True) #refers to unlimited amount

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()