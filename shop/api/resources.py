from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView, DestroyAPIView
from shop.api.serializers import MerchandiseSerializer, CreateShopBuyerSerializer, OrderSerializer, ReturnSerializer, \
    ReturnDeleteSerializer
from shop.models import Merchandise, ShopBuyer, Order, Return


class CreateShopBuyerAPIView(CreateAPIView):
    """creates an instance of a ShopBuyer and grants 1KK of cold hard cash"""
    serializer_class = CreateShopBuyerSerializer
    queryset = ShopBuyer.objects.all()
    http_method_names = ['post']


class MerchandiseViewSet(viewsets.ModelViewSet):
    """create, update, list for admin and list for authenticated users"""
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'item'
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


class ReturnViewSet(viewsets.ModelViewSet):
    """
    is used by ShopBuyer to create an instance of return if time is not up and review returns both by Admin and Buyer
    """
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    permission_classes = [permissions.IsAuthenticated]
    #http_method_names = ['post', 'get']

    def perform_destroy(self, instance):
        print('IN perform DESTROY')

    def destroy(self, request, *args, **kwargs):
        print('IN DESTROY')
        print(self)
        print(args)
        print(kwargs)


class ReturnDestroyAPIView(DestroyAPIView):
    """is used by admin to delete an instance of return """
    queryset = Return.objects.all()
    serializer_class = ReturnDeleteSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        if self.request.data.get('is_accepted', 0):
            user = ShopBuyer.objects.get(id=instance.order_to_return.buyer.id)
            product = Merchandise.objects.get(id=instance.order_to_return.merchandise.id)
            order = Order.objects.get(id=instance.order_to_return.id)
            order_value = order.get_order_value
            print(user, order, order_value, product)
            user.wallet += order_value
            product.stock += order.order_quantity
            user.save()
            product.save()
        instance.delete()


