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
