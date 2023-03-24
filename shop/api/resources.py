import datetime

from rest_framework import viewsets, permissions, serializers
from rest_framework.generics import CreateAPIView, DestroyAPIView
from shop.api.serializers import MerchandiseSerializer, CreateShopBuyerSerializer, OrderSerializer, ReturnSerializer

from shop.models import Merchandise, ShopBuyer, Order, Return


class CreateShopBuyerAPIView(CreateAPIView):
    """creates an instance of a ShopBuyer and grants 1KK of cold hard cash"""
    serializer_class = CreateShopBuyerSerializer
    queryset = ShopBuyer.objects.all()
    http_method_names = ['post']


class MerchandiseViewSet(viewsets.ModelViewSet):
    """create, update, list for admin and list for all users"""

    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class OrdersViewSet(viewsets.ModelViewSet):
    """create and list of orders instance"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(buyer=self.request.user)


class ReturnViewSet(viewsets.ModelViewSet):
    """
    is used by ShopBuyer to create an instance of return if time is not up and review returns both by Admin and Buyer
    """
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'get', 'delete']

    def get_permissions(self):
        if self.request.method in ('POST', 'GET'):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_destroy(self, instance):
        if self.request.data.get('is_accepted'):
            user = ShopBuyer.objects.get(id=instance.order_to_return.buyer.id)
            product = Merchandise.objects.get(id=instance.order_to_return.merchandise.id)
            order = Order.objects.get(id=instance.order_to_return.id)
            order_value = order.get_order_value
            user.wallet += order_value
            product.stock += order.order_quantity
            user.save()
            product.save()
        instance.delete()

    def perform_create(self, serializer):
        order_to_return = serializer.validated_data['order_to_return']
        if Return.objects.filter(id=order_to_return.id).exists():
            raise serializers.ValidationError('you have already applied for return, wait for acceptance')
        if datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=3) > order_to_return.bought_at:
            raise serializers.ValidationError('unfortunately you cant return the good, the time is up')
        return serializer.save()

