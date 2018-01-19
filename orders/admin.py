from django.contrib import admin

# Register your models here.
from orders.models import UserCheckout, UserAddress, Order


admin.site.register(Order)
admin.site.register(UserAddress)
admin.site.register(UserCheckout)
