from django.urls import path
from .views import ProductView, LogoutView, LoginView, RegisterUser, AddMerchandise, UpdateMerchandise, \
    ReturnedMerchandise, DeleteMerchandise, OrderHistory, ReviewMerchandise

app_name = 'shop'

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path('order_history/', OrderHistory.as_view(), name='order_history'),
    path('registration/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('review_merchandise/', ReviewMerchandise.as_view(), name='review_merchandise'),
    path('add_merchandise/', AddMerchandise.as_view(), name='add_merchandise'),
    path('update_merchandise/<int:pk>/', UpdateMerchandise.as_view(), name='update_merchandise'),
    path('delete_merchandise/<int:pk>/', DeleteMerchandise.as_view(), name='delete_merchandise'),
    path('returned_merchandise/', ReturnedMerchandise.as_view(), name='returned_merchandise'),
]
