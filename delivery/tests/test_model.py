from rest_framework import status

from delivery.tests.test_setup import TestSetUp
from delivery.models import User, Customer, CustomerProfile, Cart, Courier, CourierProfile, Restaurateur, \
    RestaurateurProfile


class TestRegistrationModels(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.registration_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_customer_create_profile_cart(self):
        test_user = User.objects.create(username='Test_name', password='Test_password', type=User.Types.CUSTOMER)
        self.assertTrue(Customer.objects.get(id=test_user.id))
        self.assertTrue(CustomerProfile.objects.get(user=test_user))
        self.assertTrue(Cart.objects.get(owner=test_user))

    def test_courier_create_profile(self):
        test_user = User.objects.create(username='Test_name', password='Test_password', type=User.Types.COURIER)
        self.assertTrue(Courier.objects.get(id=test_user.id))
        self.assertTrue(CourierProfile.objects.get(user=test_user))

    def test_change_user_type(self):
        self.test_user.type = User.Types.RESTAURATEUR
        self.assertTrue(self.test_user.type)

    def test_profile_create(self):
        test_user = User.objects.create(username='Test_name', password='Test_password', type=User.Types.RESTAURATEUR)
        self.assertTrue(Restaurateur.objects.get(id=test_user.id))
        self.assertTrue(RestaurateurProfile.objects.get(user=test_user))
