# Generated by Django 3.2.12 on 2022-02-14 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_phone',
            field=models.BigIntegerField(default=88888888888),
        ),
    ]
