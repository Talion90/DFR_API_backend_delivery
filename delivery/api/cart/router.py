from rest_framework import routers

from delivery.api.cart.views import CartViewSet

router = routers.SimpleRouter()
router.register('cart', CartViewSet, basename='cart')

urlpatterns = []
urlpatterns += router.urls
