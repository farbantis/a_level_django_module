from django.contrib import admin
from .models import ShopBuyer, ShopUser, ShopAdmin, Merchandise, Order, Return

admin.site.register(ShopAdmin)
admin.site.register(ShopUser)
admin.site.register(ShopBuyer)
admin.site.register(Merchandise)
admin.site.register(Order)
admin.site.register(Return)


