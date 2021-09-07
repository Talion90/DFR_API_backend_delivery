from rest_framework import permissions


class IsRestaurantOwner(permissions.BasePermission):

    message = 'Вы должны быть администратором ресторана'

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return bool(request.user and request.user.type == 'RESTAURATEUR')
        else:
            return False


class IsCourier(permissions.BasePermission):

    message = 'Вы должны быть курьером'

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return bool(request.user and request.user.type == 'COURIER')
        else:
            return False


class IsCustomer(permissions.BasePermission):

    message = 'Вы должны быть владельцем и покупателем'

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return bool(request.user and request.user.type == 'CUSTOMER')
        else:
            return False


class IsCourierOrRestaurateur(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return bool(request.user.type == 'COURIER' or request.user.type == 'RESTAURATEUR')
        else:
            return False
