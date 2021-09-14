from django.urls import path, include

from delivery.api.profiles.views import UserListAPIView, CourierDetailAPIView, CustomerDetailAPIView, \
    RestaurateurDetailAPIView
from delivery.api.restaurant.views import RestaurantCreateAPIView, RestaurantDetailAPIView, DishAPIList, \
    DishDetailAPIView, RestaurantListAPIView
from delivery.api.order.views import CustomerOrderView, ComplaintAPIView, CheckoutView

app_name = 'delivery'
urlpatterns = [
    path('restaurant/<slug:slug>/menu/<slug:slug_dish>/', DishDetailAPIView.as_view(), name='dish_detail'),
    path('restaurant/<slug:slug>/menu/', DishAPIList.as_view(), name='menu'),
    path('restaurant/<slug:slug>/', RestaurantDetailAPIView.as_view(), name='detail_restaurant'),
    path('restaurants/new/', RestaurantCreateAPIView.as_view(), 'new_restaurant'),
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurants'),
    path('restaurateur/<int:pk>/', RestaurateurDetailAPIView.as_view(), name='profile_restaurateur'),
    path('courier/<int:pk>/', CourierDetailAPIView.as_view(), name='profile_courier'),
    path('complaint/', ComplaintAPIView.as_view(), name='complaint'),
    path('customer/<int:pk>/checkout/', CheckoutView.as_view(), name='checkout'),
    path('customer/<int:pk>/orders/', CustomerOrderView.as_view(), name='customer_order'),
    path('customer/<int:pk>/', CustomerDetailAPIView.as_view(), name='profile_customer'),
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('suborder/', include('delivery.order.urls'), name='suborder'),
    path('', include('delivery.cart.router'), name='cart'),
]
