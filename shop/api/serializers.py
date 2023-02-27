from rest_framework import serializers
from shop.models import ShopBuyer, Order, Return, Merchandise


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['merchandise', 'buyer', 'order_quantity', 'bought_at']


class MerchandiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ['name', 'description', 'price', 'picture', 'stock']


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['order_to_return', 'returned_at']
