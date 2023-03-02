from rest_framework import serializers
from shop.models import ShopBuyer, Order, Return, Merchandise


class ShopBuyerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=255)
    # class Meta:
    #     model = ShopBuyer
    #     fields = ['email', ]


class MerchandiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchandise
        fields = ['id', 'name', 'description', 'price', 'picture', 'stock']


class ReturnSerializer(serializers.ModelSerializer):
    pass
    # class Meta:
    #     model = Return
    #     fields = ['order_to_return', 'returned_at']


class OrderSerializer(serializers.ModelSerializer):
    merchandise = MerchandiseSerializer(many=True)
    buyer = ShopBuyerSerializer(many=True)
    order_quantity = serializers.IntegerField()

    # class Meta:
    #     model = Order
    #     fields = ['merchandise', 'buyer', 'order_quantity', 'bought_at']
