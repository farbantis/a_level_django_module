from django.urls import path
from rest_framework import routers
from shop.api.resources import MerchandiseViewSet, CreateShopBuyerAPIView

router = routers.SimpleRouter()
router.register(r'merchandise', MerchandiseViewSet)
urlpatterns = router.urls


urlpatterns += [
    # path('add_merchandise/', MerchandiseViewSet.as_view),
    path('create_user/', CreateShopBuyerAPIView.as_view()),
]
