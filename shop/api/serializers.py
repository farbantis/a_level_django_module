from rest_framework import serializers
from shop.models import ShopBuyer, Order, Return, Merchandise
from utils.constants import INITIAL_WALLET_AMOUNT


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


class MerchandiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchandise
        fields = ['id', 'name', 'description', 'price', 'picture', 'stock']


class OrderSerializer(serializers.ModelSerializer):
    # merchandise = MerchandiseSerializer(many=True)
    # buyer = CreateShopBuyerSerializer(many=True)
    # order_quantity = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['merchandise', 'buyer', 'order_quantity', 'bought_at']


class ReturnSerializer(serializers.ModelSerializer):
    pass
    # class Meta:
    #     model = Return
    #     fields = ['order_to_return', 'returned_at']