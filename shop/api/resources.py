from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from shop.api.serializers import MerchandiseSerializer, CreateShopBuyerSerializer
from shop.models import Merchandise, ShopBuyer


class CreateShopBuyerAPIView(CreateAPIView):
    serializer_class = CreateShopBuyerSerializer
    queryset = ShopBuyer.objects.all()


class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'item'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.user.is_staff:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(MerchandiseViewSet, self).get_permissions()

