from django.db.models import F


def discount(modeladmin, request, queryset):
    """Set shares by restaurants"""
    f = F('price')
    for rec in queryset:
        rec.price = f / 2
        rec.save()
    modeladmin.message_user(request, 'Действие выполнено')
