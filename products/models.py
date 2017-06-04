from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 512)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places = 2, max_digits = 20 )
    active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.title