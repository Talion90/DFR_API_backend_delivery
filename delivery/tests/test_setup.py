from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from delivery.models import User, Restaurant, RestaurateurProfile, Dish, CartDish


class TestSetUp(APITestCase):

    def setUp(self):
        REGISTRATION_URL = 'http://127.0.0.1:8000/auth/users/'
        self.user_data = {
            'username': 'Aragorn',
            'password': 'Qwerty24',
        }
        self.test_user = User.objects.create(username='Test', password='Qwerty24')

        self.test_restaurateur = User.objects.create(
            username='Legolas',
            password='Qwerty24',
            type=User.Types.RESTAURATEUR
        )
        self.image = SimpleUploadedFile('user223226_pic633_1406805128_zgWfjLt.png',
                                        content=b'',
                                        content_type='image/jpg')
        self.test_restaurant_one = Restaurant.objects.create(
            restaurateur=RestaurateurProfile.objects.get(user=self.test_restaurateur),
            title="Test_restaurant_one",
            address="Test_address",
            website="www.test.com",
            cuisine=0,
            open_time="12:00",
            close_time="23:00",
            image=self.image,
            slug="test_restaurant_one"
        )
        self.test_restaurant_two = Restaurant.objects.create(
            restaurateur=RestaurateurProfile.objects.get(user=self.test_restaurateur),
            title="Test_restaurant_two",
            address="Test_address2",
            website="www.test2.com",
            cuisine=1,
            open_time="12:00",
            close_time="23:00",
            image=self.image,
            slug="test_restaurant_two"
        )
        self.test_dish_one = Dish.objects.create(
            restaurant=self.test_restaurant_one,
            title='test_dish_one',
            price=200,
            slug_dish='test_dish_one'
        )
        self.test_dish_two = Dish.objects.create(
            restaurant=self.test_restaurant_one,
            title='test_dish_two',
            price=100,
            slug_dish='test_dish_two'
        )
        self.test_dish_three = Dish.objects.create(
            restaurant=self.test_restaurant_two,
            title='test_dish_three',
            price=50,
            slug_dish='test_dish_three'
        )
        self.test_customer = User.objects.create(
            username='Gandalf',
            password='Qwerty24',
            type=User.Types.CUSTOMER
        )
        self.test_cart_dish = CartDish.objects.create(
        )

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
