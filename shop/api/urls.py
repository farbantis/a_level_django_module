from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from shop.api.resources import MerchandiseViewSet, CreateShopBuyerAPIView, OrdersViewSet, ReturnViewSet, ReturnDestroyAPIView

router = routers.SimpleRouter()
router.register(r'merchandise', MerchandiseViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'returns', ReturnViewSet)
urlpatterns = router.urls


urlpatterns += [
    path('create_user/', CreateShopBuyerAPIView.as_view()),
    path('login/', obtain_auth_token),
    path('destroy/<int:pk>', ReturnDestroyAPIView.as_view()),
]
