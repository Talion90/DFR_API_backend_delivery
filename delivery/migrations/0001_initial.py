# Generated by Django 3.2.6 on 2021-09-07 18:36

import delivery.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('type', models.CharField(blank=True, choices=[('CUSTOMER', 'Customer'), ('RESTAURATEUR', 'Restaurateur'), ('COURIER', 'Courier')], default=None, max_length=50, null=True, verbose_name='Тип пользователя')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_dishes', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Итого')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('delivery_address', models.CharField(max_length=200, verbose_name='Адрес доставки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения заказа')),
                ('delivery_datetime_all', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата и время доставки заказа')),
                ('payment', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Карта')], default='cash', max_length=100, verbose_name='Способ оплаты')),
                ('status_order', models.CharField(choices=[('new', 'Новый заказ'), ('payed', 'Заказ оплачен'), ('completed', 'Доставлен')], default='new', max_length=255, verbose_name='Статус заказа')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_cart', to='delivery.cart', verbose_name='Корзина')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Сайт')),
                ('cuisine', models.IntegerField(choices=[(0, 'Общий'), (1, 'Европейская'), (2, 'Азиатская'), (3, 'Фаст Фуд')], default=0)),
                ('open_time', models.TimeField(verbose_name='Время открытия')),
                ('close_time', models.TimeField(verbose_name='Время закрытия')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Изображение ресторана')),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('orders', models.ManyToManyField(blank=True, related_name='orders_restaurants', to='delivery.Order', verbose_name='Заказы ресторана')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время доставки подаказа')),
                ('status_suborder', models.CharField(choices=[('cooking', 'Готовится'), ('delivering', 'Передан курьеру'), ('completed', 'Доставлен')], default='cooking', max_length=255, verbose_name='Статус подзаказа')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий к подзаказу')),
                ('main_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_main_order', to='delivery.order', verbose_name='Заказ')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_restaurant_suborder', to='delivery.restaurant', verbose_name='Ресторан подзаказа')),
            ],
            options={
                'verbose_name': 'Подзаказ',
                'verbose_name_plural': 'Подзаказы',
            },
        ),
        migrations.CreateModel(
            name='RestaurateurProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurants', models.ManyToManyField(blank=True, related_name='related_restaurants', to='delivery.Restaurant', verbose_name='Рестораны')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurateur_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль ресторатора',
                'verbose_name_plural': 'Профили рестораторов',
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='restaurateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_restaurant', to='delivery.restaurateurprofile'),
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Цена')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Изображение блюда')),
                ('description', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Описание')),
                ('slug_dish', models.SlugField(blank=True, max_length=255)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_restaurant_dish', to='delivery.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
                'db_table': 'dish',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_address', models.CharField(max_length=255, null=True, verbose_name='Домашний адрес')),
                ('card_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Номер банковской карты')),
                ('orders', models.ManyToManyField(blank=True, related_name='related_customer', to='delivery.Order', verbose_name='Заказы покупателя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль покупателя',
                'verbose_name_plural': 'Профили покупателей',
            },
        ),
        migrations.CreateModel(
            name='CourierProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suborders', models.ManyToManyField(blank=True, related_name='related_courier_suborders', to='delivery.SubOrder', verbose_name='Подзаказы')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='courier_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль курьера',
                'verbose_name_plural': 'Профили курьеров',
            },
        ),
        migrations.CreateModel(
            name='CartDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Итоговая цена')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_dishes', to='delivery.cart', verbose_name='Корзина')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_dish', to='delivery.dish', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Блюдо корзины',
                'verbose_name_plural': 'Блюда корзины',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='dishes',
            field=models.ManyToManyField(blank=True, related_name='related_cart_dishes', to='delivery.CartDish'),
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
            ],
            options={
                'verbose_name': 'Курьер',
                'verbose_name_plural': 'Курьеры',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('delivery.user',),
            managers=[
                ('objects', delivery.models.CourierManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('delivery.user',),
            managers=[
                ('objects', delivery.models.CustomerManager()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurateur',
            fields=[
            ],
            options={
                'verbose_name': 'Ресторатор',
                'verbose_name_plural': 'Рестораторы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('delivery.user',),
            managers=[
                ('objects', delivery.models.RestaurateurManager()),
            ],
        ),
        migrations.AddField(
            model_name='suborder',
            name='courier',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.courier'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_customer', to='delivery.customer', verbose_name='Покупатель'),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст жалобы')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_complaint_order', to='delivery.order', verbose_name='Заказ')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_complaint_customer', to='delivery.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
            },
        ),
        migrations.AddField(
            model_name='cartdish',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.customer', verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_owner', to='delivery.customer', verbose_name='Владелец'),
        ),
    ]
