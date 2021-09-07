from django.utils import timezone
from django.template.loader import render_to_string

from crud_rest.settings import ALLOWED_HOSTS

from django.core.mail import send_mail


def send_notification(kind, **kwargs):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://127.0.0.1:8000'

    if kind == 'new':
        context = {
            'suborder': kwargs['suborder'],
            'dishes': kwargs['dishes'],
            'host': host,
        }
        subject = render_to_string('email/mail_subject_new_order.txt')
        body_text = render_to_string('email/mail_body_new_order.txt', context=context)
    elif kind == 'delivering':
        context = {
            'customer_username': kwargs['customer_username'],
            'suborder': kwargs['suborder'],
            'courier': kwargs['courier'],
            'courier_phone': kwargs['courier_phone'],
            'host': host,
        }
        subject = render_to_string('email/mail_subject_delivering.txt')
        body_text = render_to_string('email/mail_body_delivering.txt', context=context)
    elif kind == 'complete':
        context = {
            'customer_username': kwargs['customer_username'],
            'suborder_id': kwargs['order'],
            'host': host,
        }
        subject = render_to_string('email/mail_subject_order_complete.txt', context)
        body_text = render_to_string('email/mail_body_order_complete.txt', context=context)

    send_mail(
        subject,
        body_text,
        'frodo.baggins.ring.keeper@gmail.com',
        [kwargs['email']],  # email
        fail_silently=False,
    )


def get_delivery_datetime(qty_suborders):
    # base delivery time 30 min + 15 for each suborder
    return timezone.now() + timezone.timedelta(minutes=(15 + qty_suborders * 15))
