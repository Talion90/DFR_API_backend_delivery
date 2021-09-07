import stripe
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status, viewsets, response, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView

from ..models import Order, Customer, Cart, SubOrder, CourierProfile
from .serializers import OrderSerializer, OrderExtraSerializer, SubOrderSerializer, ComplaintSerializer, \
    CheckoutSerializer
from ..permissions import IsCourier, IsCustomer
from ..tasks import send_complete_status, send_delivery_status
from ..utilities import get_delivery_datetime


class SubOrderViewSet(viewsets.ModelViewSet):
    """List of suborders and change their status"""
    serializer_class = SubOrderSerializer
    queryset = SubOrder.objects.all().order_by('-id')

    def get_permissions(self):
        if self.action:
            permission_classes = [IsCourier]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, *args, **kwargs):
        if self.request.user.type == 'CUSTOMER':
            queryset = SubOrder.objects.filter(main_order__customer=self.request.user)
            serializer = SubOrderSerializer(queryset, many=True)
            return response.Response(serializer.data)
        elif self.request.user.type == "RESTAURATEUR":
            queryset = SubOrder.objects.filter(restaurant__restaurateur=self.request.user.restaurateur_profile)
            serializer = SubOrderSerializer(queryset, many=True)
            return response.Response(serializer.data)
        elif self.request.user.type == 'COURIER':
            q = Q(courier=None) | Q(courier=self.request.user)
            queryset = SubOrder.objects.filter(q)
            serializer = SubOrderSerializer(queryset, many=True)
            return response.Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        suborder = get_object_or_404(SubOrder, id=kwargs['pk'])
        suborder.status_suborder = request.data['status_suborder']

        # check status of order's suborders for send notification
        order = Order.objects.get(id=suborder.main_order_id)
        if suborder.status_suborder == SubOrder.STATUS_COMPLETED:
            suborder.delivery_datetime = timezone.now()
            context = {
                'email': order.customer.email,
                'customer_username': order.customer.username,
                'suborder': suborder
            }
            send_complete_status.delay('complete', **context)
        elif suborder.status_suborder == SubOrder.STATUS_DELIVERING:
            context = {
                'email': order.customer.email,
                'customer_username': order.customer.username,
                'suborder': suborder,
                'courier': suborder.courier,
                'courier_phone': suborder.courier.phone
            }
            send_delivery_status.delay('delivering', **context)
        suborder.save()

        suborders = SubOrder.objects.filter(main_order=suborder.main_order).all()

        if all([current_sub.status_suborder == SubOrder.STATUS_COMPLETED for current_sub in suborders]):
            order.status_order = Order.STATUS_COMPLETED
            order.delivery_datetime_all = suborder.delivery_datetime
            order.save()

        serializer = SubOrderSerializer(suborder)
        return response.Response(serializer.data)

    @action(methods=['patch'], detail=True)
    def courier_assign(self, request, **kwargs):
        courier_profile = CourierProfile.objects.get(user=request.user)
        suborder = SubOrder.objects.get(id=kwargs['suborder_id'])
        if not suborder.courier:
            suborder.courier = request.user
            suborder.save()
            courier_profile.suborders.add(suborder)
            return response.Response({'Курьер заказа': f'{suborder.courier}'}, status=status.HTTP_200_OK)
        return response.Response({'detail': 'Заказ уже принят другим курьером'}, status=status.HTTP_200_OK)


class CustomerOrderView(generics.ListCreateAPIView):
    """View and order creation by client"""
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer, ]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = OrderExtraSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')

    @transaction.atomic
    def perform_create(self, serializer):
        customer = Customer.objects.get(id=self.request.user.id)
        cart = Cart.objects.filter(owner=customer).first()
        cart.in_order = True
        cart.save()
        qty_restaurants = len(set([cart.dish.restaurant for cart in cart.dishes.all()]))
        serializer.save(customer=customer, cart=cart, delivery_datetime_all=get_delivery_datetime(qty_restaurants))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ComplaintAPIView(generics.CreateAPIView):
    """Creation a complaint by client"""
    serializer_class = ComplaintSerializer
    permission_classes = [IsCustomer, ]

    def perform_create(self, serializer):
        customer = Customer.objects.filter(id=self.request.user.id).first()
        order = Order.objects.filter(owner=customer).last()
        serializer.save(customer=customer, order=order)


class CheckoutView(APIView):
    """Checkout for making payment in stripe system"""
    permission_classes = [IsCustomer, ]
    queryset = Order.objects.all()
    serializer_class = CheckoutSerializer

    def get(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51JQxw4FsroFErJ3HeqTqvMYHlrtfWyuVBkAdpgLhFOJJzuTUfsR7oklMWKSKf29QXQfgjt84iKvoNnRl2QmTCFrn00P3k5TPOv "
        intent = stripe.PaymentIntent.create(
            amount=int(self.request.cart.final_price * 100),
            currency='usd',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )
        request.serializer.client_secret = intent.client_secret
        return response.Response(self, request, *args, **kwargs)

    # @transaction.atomic
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
