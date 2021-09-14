from rest_framework.decorators import action
from rest_framework import response, status, viewsets

from django.shortcuts import get_object_or_404

from delivery.api.cart.serializers import CartSerializer
from delivery.api.cart.utils import recalc_cart
from delivery.models import Cart, Dish, CartDish, Customer
from delivery.permissions import IsCustomer


class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsCustomer]

    @staticmethod
    def get_cart(user):
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(owner=user, for_anonymous_user=False)
            if created:
                cart.save()
            return cart
        else:
            return Cart.objects.filter(for_anonymous_user=True).first()

    @staticmethod
    def _get_or_create_cart_dish(customer: Customer, cart: Cart, dish: Dish):
        cart_dish, created = CartDish.objects.get_or_create(
            customer=customer,
            dish=dish,
            cart=cart
        )
        return cart_dish, created

    @action(methods=["get"], detail=False)
    def current_customer_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        cart_serializer = CartSerializer(cart)
        return response.Response(cart_serializer.data)

    @action(
        methods=['put'],
        detail=False,
        url_path=r'current_customer_cart/add_to_cart/(?P<dish_id>\d+)'
    )
    def dish_add_to_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        dish = get_object_or_404(Dish, id=kwargs['dish_id'])
        cart_dish, created = self._get_or_create_cart_dish(customer=self.request.user, cart=cart, dish=dish)
        if created:
            cart.dishes.add(cart_dish)
            recalc_cart(cart)
            return response.Response({'detail': 'Dish add to the cart'}, status=status.HTTP_200_OK)
        return response.Response({'detail': 'Dish has been already in cart'}, status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['patch'],
        detail=False,
        url_path=r'current_customer_cart/change_qty/(?P<quantity>\d+)/(?P<cart_dish_id>\d+)'
    )
    def dish_change_quantity(self, *args, **kwargs):
        cart_dish = get_object_or_404(CartDish, id=kwargs['cart_dish_id'])
        cart_dish.quantity = int(kwargs['quantity'])
        cart_dish.save()
        recalc_cart(cart_dish.cart)
        return response.Response(f'Quantity has been changed {cart_dish.quantity}', status=status.HTTP_200_OK)

    @action(
        methods=['put'],
        detail=False,
        url_path=r'current_customer_cart/remove_from_cart/(?P<cart_dish_id>\d+)'
    )
    def dish_remove_from_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request.user)
        cart_dish = get_object_or_404(CartDish, id=kwargs['cart_dish_id'])
        cart.dishes.remove(cart_dish)
        cart_dish.delete()
        recalc_cart(cart)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
