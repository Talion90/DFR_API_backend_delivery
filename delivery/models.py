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
        verbose_name='Тип пользователя'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class CustomerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

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
        verbose_name='Домашний адрес',
        null=True
    )
    card_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер банковской карты',
        blank=True,
        null=True
    )
    orders = models.ManyToManyField(
        'Order',
        blank=True,
        verbose_name='Заказы покупателя',
        related_name='related_customer'
    )

    def __str__(self):
        return f'Профиль покупателя {self.user.username}'

    class Meta:
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателей'


class Cart(models.Model):
    owner = models.ForeignKey(
        Customer,
        null=True,
        verbose_name='Владелец',
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
        verbose_name='Итого'
    )
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f'Коризина {self.owner}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CourierManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COURIER)


class Courier(User):
    base_type = User.Types.COURIER
    objects = CourierManager()

    class Meta:
        proxy = True
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

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
        verbose_name='Подзаказы',
        blank=True
    )

    def __str__(self):
        return f'Курьер {self.user.username}'

    class Meta:
        verbose_name = 'Профиль курьера'
        verbose_name_plural = 'Профили курьеров'


class RestaurateurManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.RESTAURATEUR)


class Restaurateur(User):
    base_type = User.Types.RESTAURATEUR
    objects = RestaurateurManager()

    class Meta:
        proxy = True
        verbose_name = 'Ресторатор'
        verbose_name_plural = 'Рестораторы'

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
        verbose_name='Рестораны',
        blank=True
    )

    def __str__(self):
        return f'Ресторатор {self.user.username}'

    class Meta:
        verbose_name = 'Профиль ресторатора'
        verbose_name_plural = 'Профили рестораторов'


class Restaurant(models.Model):
    restaurateur = models.ForeignKey(
        RestaurateurProfile,
        on_delete=models.CASCADE,
        related_name='related_restaurant',
        null=True
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес'
    )
    website = models.URLField(
        verbose_name='Сайт',
        blank=True,
        null=True
    )
    CUISINE_TYPE = (
        (0, 'Общий'),
        (1, 'Европейская'),
        (2, 'Азиатская'),
        (3, 'Фаст Фуд')
    )
    cuisine = models.IntegerField(
        choices=CUISINE_TYPE,
        default=0
    )
    open_time = models.TimeField(verbose_name='Время открытия')
    close_time = models.TimeField(verbose_name='Время закрытия')
    image = models.ImageField(
        verbose_name='Изображение ресторана',
        blank=True
    )
    orders = models.ManyToManyField(
        'Order',
        related_name='orders_restaurants',
        verbose_name='Заказы ресторана',
        blank=True,
    )
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    @property
    def dishes(self):
        return json.dumps(Dish.objects.filter(restaurant=self).values())

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'
        ordering = ['-title']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Dish(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='Ресторан',
        null=True,
        related_name='related_restaurant_dish'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        verbose_name='Цена'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        blank=True
    )
    description = models.TextField(
        max_length=5000,
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    slug_dish = models.SlugField(
        max_length=255,
        blank=True
    )

    class Meta:
        db_table = 'dish'
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
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
        verbose_name='Покупатель'
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        related_name='related_dishes'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
        related_name='related_dish'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    final_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Итоговая цена'
    )

    def __str__(self):
        return f'Блюдо: {self.dish.title} (для корзины)'

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.dish.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блюдо корзины'
        verbose_name_plural = 'Блюда корзины'


class Order(models.Model):
    PAYMENT_CASH = 'cash'
    PAYMENT_CARD = 'card'
    PAYMENT_CHOICE = (
        (PAYMENT_CASH, 'Наличные'),
        (PAYMENT_CARD, 'Карта')
    )
    STATUS_NEW = 'new'
    STATUS_PAYED = 'payed'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICE = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_PAYED, 'Заказ оплачен'),
        (STATUS_COMPLETED, 'Доставлен')
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
        related_name='related_customer'
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name='Корзина',
        related_name='related_cart',
        null=True,
        blank=True
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Фамилия',
    )
    delivery_address = models.CharField(
        max_length=200,
        verbose_name='Адрес доставки'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата размещения заказа',
        auto_now_add=True,
    )
    delivery_datetime_all = models.DateTimeField(
        verbose_name='Дата и время доставки заказа',
        default=None,
        null=True,
        blank=True
    )
    payment = models.CharField(
        max_length=100,
        choices=PAYMENT_CHOICE,
        default=PAYMENT_CASH,
        verbose_name='Способ оплаты'
    )
    status_order = models.CharField(
        max_length=255,
        choices=STATUS_CHOICE,
        default=STATUS_NEW,
        verbose_name='Статус заказа'
    )

    def __str__(self):
        return f'Заказ №{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class SubOrder(models.Model):
    STATUS_IN_RESTAURANT = 'cooking'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICE = (
        (STATUS_IN_RESTAURANT, 'Готовится'),
        (STATUS_DELIVERING, 'Передан курьеру'),
        (STATUS_COMPLETED, 'Доставлен')
    )
    main_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='related_main_order',
        verbose_name='Заказ'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='related_restaurant_suborder',
        verbose_name='Ресторан подзаказа',
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
        verbose_name='Дата и время доставки подаказа',
        blank=True,
        null=True
    )
    status_suborder = models.CharField(
        max_length=255,
        choices=STATUS_CHOICE,
        default=STATUS_IN_RESTAURANT,
        verbose_name='Статус подзаказа'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий к подзаказу')

    def __str__(self):
        return f'Подзаказ №{self.id}'

    class Meta:
        verbose_name = 'Подзаказ'
        verbose_name_plural = 'Подзаказы'


class Complaint(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='related_complaint_customer',
        verbose_name='Покупатель'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='related_complaint_order',
        verbose_name='Заказ'
    )
    text = models.TextField(verbose_name='Текст жалобы')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
