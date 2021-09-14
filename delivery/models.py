import json

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from pytils.translit import slugify


class User(AbstractUser):

    objects = UserManager()

    class Types(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        RESTAURATEUR = 'RESTAURATEUR', 'Restaurateur'
        COURIER = 'COURIER', 'Courier'

    type = models.CharField(
        max_length=50,
        choices=Types.choices,
        blank=True,
        default=None,
        null=True,
        verbose_name="User type"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Phone number'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class CustomerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
        super().save(*args, **kwargs)

    @property
    def profile(self):
        return self.customerprofile


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile')
    home_address = models.CharField(
        max_length=255,
        verbose_name='Home address',
        null=True
    )
    card_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Card number',
        blank=True,
        null=True
    )
    orders = models.ManyToManyField(
        'Order',
        blank=True,
        related_name='related_customer'
    )

    def __str__(self):
        return f"Customer's profile {self.user.username}"

    class Meta:
        verbose_name = 'Profile of courier'
        verbose_name_plural = "Profile of couriers"


class Cart(models.Model):
    owner = models.ForeignKey(
        Customer,
        null=True,
        verbose_name='cart owner',
        on_delete=models.CASCADE,
        related_name='related_owner'
    )
    dishes = models.ManyToManyField(
        'CartDish',
        blank=True,
        related_name='related_cart_dishes'
    )
    total_dishes = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=8,
        default=0,
        decimal_places=2,
        verbose_name='Total'
    )
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner}'s cart"

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CourierManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COURIER)


class Courier(User):
    base_type = User.Types.COURIER
    objects = CourierManager()

    class Meta:
        proxy = True
        verbose_name = 'Courier'
        verbose_name_plural = 'Couriers'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.COURIER
        return super().save(*args, **kwargs)


class CourierProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='courier_profile'
    )
    suborders = models.ManyToManyField(
        'SubOrder',
        related_name='related_courier_suborders',
        verbose_name='Suborders',
        blank=True
    )

    def __str__(self):
        return f'Courier {self.user.username}'

    class Meta:
        verbose_name = 'Profile of courier'
        verbose_name_plural = 'Profiles of couriers'


class RestaurateurManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.RESTAURATEUR)


class Restaurateur(User):
    base_type = User.Types.RESTAURATEUR
    objects = RestaurateurManager()

    class Meta:
        proxy = True
        verbose_name = 'Restaurateur'
        verbose_name_plural = 'Restaurateurs'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.Restaurateur
        return super().save(*args, **kwargs)

    @property
    def profile(self):
        return self.restaurateurprofile


class RestaurateurProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='restaurateur_profile'
    )
    restaurants = models.ManyToManyField(
        'Restaurant',
        related_name='related_restaurants',
        verbose_name='Restaurants',
        blank=True
    )

    def __str__(self):
        return f'Restaurateur {self.user.username}'

    class Meta:
        verbose_name = 'Restaurateur profile'
        verbose_name_plural = 'Restaurateur profiles'


class Restaurant(models.Model):
    restaurateur = models.ForeignKey(
        RestaurateurProfile,
        on_delete=models.CASCADE,
        related_name='related_restaurant',
        null=True
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Title'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Address'
    )
    website = models.URLField(
        verbose_name='Website',
        blank=True,
        null=True
    )
    CUISINE_TYPE = (
        (0, 'Common'),
        (1, 'European'),
        (2, 'Asian'),
        (3, 'Fast food')
    )
    cuisine = models.IntegerField(
        choices=CUISINE_TYPE,
        default=0
    )
    open_time = models.TimeField(verbose_name='Open time')
    close_time = models.TimeField(verbose_name='Close time')
    image = models.ImageField(
        verbose_name='Picture of restaurant',
        blank=True
    )
    orders = models.ManyToManyField(
        'Order',
        related_name='orders_restaurants',
        verbose_name='restaurant orders',
        blank=True,
    )
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    @property
    def dishes(self):
        return json.dumps(Dish.objects.filter(restaurant=self).values())

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        ordering = ['-title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Dish(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='restaurant',
        null=True,
        related_name='related_restaurant_dish'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        verbose_name='price'
    )
    image = models.ImageField(
        verbose_name='dish image',
        blank=True
    )
    description = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        verbose_name='description'
    )
    slug_dish = models.SlugField(
        max_length=255,
        blank=True
    )

    class Meta:
        db_table = 'dish'
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'
        ordering = ['-title']

    def save(self, *args, **kwargs):
        self.slug_dish = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CartDish(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='customer'
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        verbose_name='cart',
        related_name='related_dishes'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='dish',
        related_name='related_dish'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='quantity'
    )
    final_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Total price'
    )

    def __str__(self):
        return f'Dish: {self.dish.title} (for cart)'

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.dish.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart dish'
        verbose_name_plural = 'Cart dishes'


class Order(models.Model):
    PAYMENT_CASH = 'cash'
    PAYMENT_CARD = 'card'
    PAYMENT_CHOICE = (
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_CARD, 'Card')
    )
    STATUS_NEW = 'new'
    STATUS_PAYED = 'payed'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICE = (
        (STATUS_NEW, 'New order'),
        (STATUS_PAYED, 'Paid order'),
        (STATUS_COMPLETED, 'Deliveried')
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='customer',
        related_name='related_customer'
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='cart',
        related_name='related_cart',
        null=True,
        blank=True
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name='name',
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='last name',
    )
    delivery_address = models.CharField(
        max_length=200,
        verbose_name='delivery address'
    )
    created_at = models.DateTimeField(
        verbose_name='date of order creation',
        auto_now_add=True,
    )
    delivery_datetime_all = models.DateTimeField(
        verbose_name='delivery datetime',
        default=None,
        null=True,
        blank=True
    )
    payment = models.CharField(
        max_length=100,
        choices=PAYMENT_CHOICE,
        default=PAYMENT_CASH,
        verbose_name='payment method'
    )
    status_order = models.CharField(
        max_length=255,
        choices=STATUS_CHOICE,
        default=STATUS_NEW,
        verbose_name='status'
    )

    def __str__(self):
        return f'Order №{self.id}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class SubOrder(models.Model):
    STATUS_IN_RESTAURANT = 'cooking'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICE = (
        (STATUS_IN_RESTAURANT, 'Cooking'),
        (STATUS_DELIVERING, 'Handed over to the courier'),
        (STATUS_COMPLETED, 'Delivered')
    )
    main_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='related_main_order',
        verbose_name='order'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='related_restaurant_suborder',
        verbose_name='suborder restaurant',
        null=True
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    delivery_datetime = models.DateTimeField(
        verbose_name='suborder delivery datetime',
        blank=True,
        null=True
    )
    status_suborder = models.CharField(
        max_length=255,
        choices=STATUS_CHOICE,
        default=STATUS_IN_RESTAURANT,
        verbose_name='status suborder'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='comment')

    def __str__(self):
        return f'suborder №{self.id}'

    class Meta:
        verbose_name = 'Suborder'
        verbose_name_plural = 'Suborders'


class Complaint(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='related_complaint_customer',
        verbose_name='customer'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='related_complaint_order',
        verbose_name='order'
    )
    text = models.TextField(verbose_name='complain text')

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
