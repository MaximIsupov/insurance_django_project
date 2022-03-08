from django.db import models
# Create your models here.


class Company(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class Category(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Наименование категории')


class Product(models.Model):
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    percentage = models.FloatField(default=0)
    period = models.FloatField(default=0)


class Order(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer_first_name = models.CharField(max_length=50)
    customer_middle_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_phone = models.BigIntegerField(default=88888888888)
    customer_mail = models.CharField(max_length=100)

