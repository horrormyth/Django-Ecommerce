from django.contrib import admin

# Register your models here.
from orders.models import UserCheckout, UserAddress

admin.site.register(UserAddress)
admin.site.register(UserCheckout)
