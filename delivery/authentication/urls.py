from django.urls import path
from delivery.authentication.views import RegistrationAPIView, LoginAPIView


app_name = 'authentication'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
