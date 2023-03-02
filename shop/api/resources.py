from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from shop.api.serializers import MerchandiseSerializer
from shop.models import Merchandise


class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'item'


class MerchandiseCreateAPIView(CreateAPIView):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
