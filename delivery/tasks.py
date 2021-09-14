from crud_rest.celery import app

from delivery.utilities import send_notification


@app.task
def send_new_suborder(kind, **kwargs):
    send_notification(kind, **kwargs)


@app.task
def send_delivery_status(kind, **kwargs):
    send_notification(kind, **kwargs)


@app.task
def send_complete_status(kind, **kwargs):
    send_notification(kind, **kwargs)
