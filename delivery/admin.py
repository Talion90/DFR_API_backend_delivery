from django.contrib import admin
from django.db.models import F

from delivery.models import Restaurant, Dish, CartDish, Courier, User, Restaurateur, RestaurateurProfile, Customer, \
    CustomerProfile, Cart, Order, SubOrder, CourierProfile, Complaint


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'restaurateur', 'title',
        'address', 'website',
        'cuisine', 'open_time', 'close_time',
        'slug',
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    actions = ('discount',)
    list_display = ("id", "title", "price", "restaurant", "slug_dish")
    search_fields = ('title', 'restaurant', 'price')
    prepopulated_fields = {'slug_dish': ('title',)}

    def discount(modeladmin, request, queryset):
        f = F('price')
        for rec in queryset:
            rec.price = f / 2
            rec.save()
        modeladmin.message_user(request, 'Действие выполнено')


@admin.register(CartDish)
class CartDishAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "dish", "quantity", "final_price")


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


admin.site.register(User)
admin.site.register(Restaurateur)
admin.site.register(RestaurateurProfile)
admin.site.register(Customer)
admin.site.register(CustomerProfile)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(SubOrder)
admin.site.register(CourierProfile)
admin.site.register(Complaint)
