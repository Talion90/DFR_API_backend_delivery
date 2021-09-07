from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from delivery.order.views import SubOrderViewSet

suborder_list = SubOrderViewSet.as_view({
    'get': 'list',
})

suborder_detail = SubOrderViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})
courier_assign = SubOrderViewSet.as_view({
    'patch': 'courier_assign'
})

urlpatterns = format_suffix_patterns([
    path('suborders/', suborder_list, name='suborder-list'),
    path('<int:pk>/', suborder_detail, name='suborder-detail'),
    path('<int:suborder_id>/courier/assign/', courier_assign, name='courier-assign'),
])
