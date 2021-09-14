from rest_framework import serializers

from delivery.models import Restaurant, Dish


class RestaurantSerializer(serializers.ModelSerializer):

    phone = serializers.SerializerMethodField()
    restaurateur = serializers.SerializerMethodField()
    cuisine = serializers.SerializerMethodField()

    @staticmethod
    def get_cuisine(obj):
        cuisine = Restaurant.CUISINE_TYPE[obj.cuisine][1]
        return str(cuisine)

    @staticmethod
    def get_restaurateur(obj):
        try:
            restaurateur = obj.restaurateur.user.username
        except AttributeError:
            return str({'restaurateur': 'restaurateur not identified'})
        return str(restaurateur)

    @staticmethod
    def get_phone(obj):
        try:
            phone = obj.restaurateur.user.phone
        except AttributeError:
            return str({'phone': 'restaurateur not identified'})
        return str(phone)

    class Meta:
        model = Restaurant
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):

    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = '__all__'

    @staticmethod
    def get_restaurant(obj):
        return str(obj.restaurant)


class RestaurantDetailSerializer(serializers.ModelSerializer):

    dishes = DishSerializer()

    class Meta:
        model = Restaurant
        fields = '__all__'
