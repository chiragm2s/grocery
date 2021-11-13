from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(products)
admin.site.register(QuantityVariant)
admin.site.register(Cart)
admin.site.register(orders)
admin.site.register(delivery)
admin.site.register(delivery_assigned)