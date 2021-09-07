from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import response, status

from delivery.models import Order, SubOrder, CartDish, User, CustomerProfile, CourierProfile, RestaurateurProfile, \
    Cart
from delivery.tasks import send_new_suborder


@receiver(post_save, sender=Order)
def create_suborder(sender, instance, created, **kwargs):
    if created:
        restaurants = set([cart.dish.restaurant for cart in instance.cart.related_dishes.all()])
        for restaurant in restaurants:
            SubOrder.objects.create(main_order=instance, restaurant=restaurant)
    else:
        return response.Response(status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=CustomerProfile)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance.user)


@receiver(post_save, sender=Order)
def zeroing_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance.customer)


@receiver(post_save, sender=SubOrder)
def send_new_suborder_to_restaurant(sender, instance, created, **kwargs):
    if created:
        suborder = SubOrder.objects.last()
        dishes = CartDish.objects.filter(dish__restaurant=instance.restaurant)
        dishes_title = [cart_dish.dish.title for cart_dish in dishes]
        context = {
            'suborder': suborder.id,
            'dishes': dishes_title,
            'email': suborder.restaurant.restaurateur.user.email
        }
        send_new_suborder.delay('new', **context)


@receiver(post_save, sender=User)
def profile_create(sender, instance, created, **kwargs):
    if created:
        if instance.type == User.Types.CUSTOMER:
            CustomerProfile.objects.create(user=instance)
        elif instance.type == User.Types.COURIER:
            CourierProfile.objects.create(user=instance)
        elif instance.type == User.Types.RESTAURATEUR:
            RestaurateurProfile.objects.create(user=instance)
