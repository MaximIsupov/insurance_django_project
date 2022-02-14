# Generated by Django 3.2.12 on 2022-02-12 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percentage', models.FloatField(default=0)),
                ('period', models.FloatField(default=0)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.category')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_first_name', models.CharField(max_length=50)),
                ('customer_middle_name', models.CharField(max_length=50)),
                ('customer_last_name', models.CharField(max_length=50)),
                ('customer_phone', models.IntegerField(default=88888888888)),
                ('customer_mail', models.CharField(max_length=100)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.product')),
            ],
        ),
    ]