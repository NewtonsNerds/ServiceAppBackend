from __future__ import absolute_import

from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_email(subject, body, from_address, to_addresses):
    send_mail(subject, body, from_address, to_addresses, fail_silently=False)
    return "Sent email"
