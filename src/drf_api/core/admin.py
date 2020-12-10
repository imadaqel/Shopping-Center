from django.contrib import admin

# Register your models here.

from .models import *
# from .models import *

admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
admin.site.register(Payment)