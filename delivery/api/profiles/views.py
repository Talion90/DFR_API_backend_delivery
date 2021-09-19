from rest_framework.permissions import IsAdminUser
from rest_framework import generics

from delivery.models import User, CourierProfile, CustomerProfile, RestaurateurProfile
from delivery.api.profiles.serializers import CourierProfileDetailSerializer, \
    CustomerProfileDetailSerializer, RestaurateurProfileDetailSerializer
from delivery.permissions import IsCourier, IsCustomer, IsRestaurantOwner


class CourierDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CourierProfileDetailSerializer
    queryset = CourierProfile.objects.all()
    permission_classes = (IsCourier, )


class CustomerDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileDetailSerializer
    queryset = CustomerProfile.objects.all()
    permission_classes = (IsCustomer, )


class RestaurateurDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = RestaurateurProfile.objects.all()
    serializer_class = RestaurateurProfileDetailSerializer
    permission_classes = (IsRestaurantOwner, )
