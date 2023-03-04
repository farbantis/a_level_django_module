from rest_framework import serializers
from shop.models import ShopBuyer, Order, Return, Merchandise
from utils.constants import INITIAL_WALLET_AMOUNT


# 1) create - OK
class CreateShopBuyerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ShopBuyer
        fields = ('id', 'username', 'password', 'wallet')
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        shop_buyer = ShopBuyer.objects.create_user(**validated_data)
        shop_buyer.wallet = INITIAL_WALLET_AMOUNT
        shop_buyer.save()
        return shop_buyer


# 1) list ok, 2) retrieve ok, 3) patch ok, 4) create ???
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
    #buyer = ShopBuyerSerializer(many=True)
    order_quantity = serializers.IntegerField()

    # class Meta:
    #     model = Order
    #     fields = ['merchandise', 'buyer', 'order_quantity', 'bought_at']
