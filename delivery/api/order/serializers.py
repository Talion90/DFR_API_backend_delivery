from rest_framework import serializers

from delivery.models import Order, SubOrder, CartDish, Complaint
from delivery.api.cart.serializers import CartOrderSerializer, CartDishSerializer


class OrderExtraSerializer(serializers.ModelSerializer):

    status_order = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    cart = CartOrderSerializer()

    @staticmethod
    def get_owner(obj):
        return str(obj.customer)

    @staticmethod
    def get_status_order(obj):
        return str(obj.status_order)

    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    status_order = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()

    @staticmethod
    def get_cart(obj):
        return str(obj.cart)

    @staticmethod
    def get_customer(obj):
        return str(obj.customer)

    @staticmethod
    def get_status_order(obj):
        return str(obj.status_order)

    class Meta:
        model = Order
        fields = '__all__'


class SubOrderSerializer(serializers.ModelSerializer):

    restaurant = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    status_suborder = serializers.SerializerMethodField()

    @staticmethod
    def get_info(obj):
        dishes = CartDish.objects.filter(dish__restaurant=obj.restaurant)
        serializer = CartDishSerializer(instance=dishes, many=True)
        return serializer.data

    @staticmethod
    def get_restaurant(obj):
        return str(obj.restaurant)

    @staticmethod
    def get_status_suborder(obj):
        return str(obj.status_suborder)

    class Meta:
        model = SubOrder
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = '__all__'


class CheckoutSerializer(serializers.ModelSerializer):

    client_secret = serializers.CharField(max_length=255)

    class Meta:
        model = Order
        fields = '__all__'
