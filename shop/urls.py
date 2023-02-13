from django.urls import path
from .views import ProductView, RegisterUserView, AddMerchandiseView, UpdateMerchandiseView, \
    ReturnedMerchandiseView, OrderHistoryView, ReviewMerchandiseView, UserLoginView, UserLogoutView

app_name = 'shop'

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('review_merchandise/', ReviewMerchandiseView.as_view(), name='review_merchandise'),
    path('add_merchandise/', AddMerchandiseView.as_view(), name='add_merchandise'),
    path('update_merchandise/<int:pk>/', UpdateMerchandiseView.as_view(), name='update_merchandise'),
    path('returned_merchandise/', ReturnedMerchandiseView.as_view(), name='returned_merchandise'),
]
