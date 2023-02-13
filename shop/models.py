from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class ShopUser(AbstractUser):
    pass


class ShopAdmin(ShopUser):
    pass


class ShopBuyer(ShopUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.username}"

    def deduct_money(self, amount):
        return self.wallet - amount


class Merchandise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.009)])
    picture = models.ImageField(upload_to='pictures/%Y/%m', blank=True, null=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:update_merchandise', kwargs={'pk': self.pk})


class Order(models.Model):
    merchandise = models.ForeignKey(Merchandise, on_delete=models.PROTECT)
    buyer = models.ForeignKey(ShopBuyer, on_delete=models.PROTECT)
    order_quantity = models.PositiveIntegerField()
    bought_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer} bought {self.order_quantity}pc of {self.merchandise} on {self.bought_at} '

    @property
    def is_merchandise_in_stock(self):
        if self.merchandise.stock >= self.order_quantity:
            return True
        return False

    @property
    def is_enough_money(self):
        if self.buyer.wallet < self.order_quantity * self.merchandise.price:
            return False
        return True

    @property
    def get_order_value(self):
        return self.order_quantity * self.merchandise.price


class Return(models.Model):
    order_to_return = models.OneToOneField(Order, on_delete=models.CASCADE)
    returned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order_to_return}'
