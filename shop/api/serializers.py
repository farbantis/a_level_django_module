import datetime
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

    class Meta:
        model = Order
        fields = ['id', 'merchandise', 'buyer', 'order_quantity', 'bought_at']

    def create(self, validated_data):
        buyer = validated_data['buyer']
        merchandise = validated_data['merchandise']
        order_quantity = validated_data['order_quantity']
        new_order_amount = order_quantity * merchandise.price
        if new_order_amount > buyer.wallet:
            raise serializers.ValidationError('not enough money')
        if order_quantity > merchandise.stock:
            raise serializers.ValidationError('not enough stock')
        new_order = Order.objects.create(
            merchandise_id=merchandise.id,
            buyer_id=buyer.id,
            order_quantity=order_quantity,
                        )
        buyer.wallet -= new_order_amount
        merchandise.stock -= order_quantity
        buyer.save()
        merchandise.save()
        return new_order


class ReturnSerializer(serializers.ModelSerializer):
    is_accepted = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Return
        fields = ('id', 'order_to_return', 'returned_at', 'is_accepted')

    # def create(self, validated_data):
    #     order_to_return = validated_data['order_to_return']
    #     if Return.objects.filter(id=order_to_return.id).exists():
    #         raise serializers.ValidationError('you have already applied for return, wait for acceptance')
    #     if datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=3) > order_to_return.bought_at:
    #         raise serializers.ValidationError('unfortunately you cant return the good, the time is up')
    #     return super().create(validated_data)
