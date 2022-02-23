import os

from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from insurance_django_project.settings import SENDGRID_API_KEY


@shared_task
def send_email_task(order, to_email):
    date = datetime.date.today()
    message = Mail(
        from_email='maksimm290100@gmail.com',
        to_emails=to_email,
        subject='Поступил новый заказ!',
        html_content=f'<strong>ФИО</strong>: {order.customer_middle_name} {order.customer_first_name} {order.customer_last_name}.<br>'
                     f'<strong>Название услуги</strong>: {order.product_id.name}.<br>'
                     f'<strong>Дата</strong>: {date}.<br>'
                     f'<strong>Контактные данные</strong>:<br>'
                     f'<strong>Номер телефона</strong>: {order.customer_phone},<br>'
                     f'<strong>Электронная почта:{order.customer_mail}.')
    try:
        sg = SendGridAPIClient(os.environ.get(SENDGRID_API_KEY))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)