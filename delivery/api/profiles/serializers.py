from rest_framework import serializers

from delivery.models import User, Courier, CourierProfile, Customer, CustomerProfile, Restaurateur, RestaurateurProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = 'user_user'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
        ref_name = 'user_customer'


class CustomerProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        return str(obj.user)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
        ref_name = 'User_customer_profile'


class CustomerProfileDetailSerializer(serializers.ModelSerializer):

    user = CustomerSerializer()

    class Meta:
        model = CourierProfile
        fields = '__all__'
        ref_name = 'User_customer_profile_det'


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
        ref_name = 'user_courier'


class CourierProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        return str(obj.user)

    class Meta:
        model = CourierProfile
        fields = '__all__'
        ref_name = 'User_courier_profile'


class CourierProfileDetailSerializer(serializers.ModelSerializer):

    user = CourierSerializer()

    class Meta:
        model = CourierProfile
        fields = '__all__'
        ref_name = 'User_courier_profile_det'


class RestaurateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurateur
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
        ref_name = 'user_restaurateur'


class RestaurateurProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        return str(obj.user)

    class Meta:
        model = RestaurateurProfile
        fields = '__all__'
        ref_name = 'User_restaurateur_profile'


class RestaurateurProfileDetailSerializer(serializers.ModelSerializer):

    user = CourierSerializer()

    class Meta:
        model = RestaurateurProfile
        fields = '__all__'
        ref_name = 'User_restaurateur_profile_det'
