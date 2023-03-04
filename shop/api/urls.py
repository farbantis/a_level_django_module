from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from shop.api.resources import MerchandiseViewSet, CreateShopBuyerAPIView, OrdersAPIView

router = routers.SimpleRouter()
router.register(r'merchandise', MerchandiseViewSet)
urlpatterns = router.urls


urlpatterns += [
    path('create_user/', CreateShopBuyerAPIView.as_view()),
    path('login/', obtain_auth_token),
    path('orders/', OrdersAPIView.as_view({'get': 'list'})),
]
