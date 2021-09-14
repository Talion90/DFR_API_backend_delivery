from rest_framework import serializers
from delivery.models import CartDish, Cart, Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CartDishSerializer(serializers.ModelSerializer):

    dish = serializers.SerializerMethodField()

    @staticmethod
    def get_dish(obj):
        return str(obj.dish)

    class Meta:
        model = CartDish
        fields = ('dish', 'quantity', 'final_price')


class CartSerializer(serializers.ModelSerializer):

    dishes = CartDishSerializer(many=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ('for_anonymous_user', )

    @staticmethod
    def get_owner(obj):
        return str(obj.owner)


class CartOrderSerializer(serializers.ModelSerializer):

    dishes = CartDishSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('dishes', 'total_dishes', 'final_price')
