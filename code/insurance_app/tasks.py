import time

from celery import shared_task
from django.core.mail import send_mail
import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task()
def send_email_task(order, to_email):
    date = datetime.date.today()
    subject = 'Поступил новый заказ!'
    html_message = render_to_string('mail_template.html', {'order': order,
                                                           'date': date})
    plain_message = strip_tags(html_message)
    from_email = 'maksimm290100@gmail.com'
    to = [to_email, ]
    return send_mail(
            subject,
            plain_message,
            from_email,
            to,
            fail_silently=False,
            html_message=html_message,
        )

