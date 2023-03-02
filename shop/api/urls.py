from django.urls import path
from rest_framework import routers
from shop.api.resources import MerchandiseViewSet, MerchandiseCreateAPIView

router = routers.SimpleRouter()
router.register(r'merchandise', MerchandiseViewSet)
urlpatterns = router.urls


urlpatterns += [
    path('add_merchandise/', MerchandiseCreateAPIView.as_view)
]
