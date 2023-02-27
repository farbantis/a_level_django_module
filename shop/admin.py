from django.contrib import admin
from .models import ShopBuyer, Merchandise, Order, Return


admin.site.register(ShopBuyer)
admin.site.register(Merchandise)
admin.site.register(Order)
admin.site.register(Return)


