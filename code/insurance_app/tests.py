from django.test import TestCase
from django.urls import reverse

from .models import Product, Company, Category, Order
from django.contrib.auth.models import User


class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company = Company.objects.create(name='company', user_id=1, description='default description')
        category = Category.objects.create(name='category')
        number_of_products = 10
        for product_num in range(number_of_products):
            Product.objects.create(company_id=company,
                                   category_id=category,
                                   name=product_num,
                                   percentage=13,
                                   period=3)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('products'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('products'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'product_list.html')

    def test_lists_all_products(self):
        resp = self.client.get(reverse('products'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['product_list']), 10)

    def test_add_product(self):
        company = Company.objects.first()
        category = Category.objects.first()
        product_data = {
            'company_id': company.pk,
            'category_id': category.pk,
            'product_name': 'test_add_product',
            'percentage': 13,
            'period': 3,
        }
        self.client.post(reverse('add_product', kwargs={'company_id': company.pk}),
                         data=product_data)
        resp = self.client.get(reverse('products'))
        self.assertEqual(len(resp.context['product_list']), 11)

    def test_edit_product(self):
        product = Product.objects.first()
        product_data = {
            'company_id': product.company_id.pk,
            'category_id': product.category_id.pk,
            'product_name': 'edit_add_product',
            'percentage': 13,
            'period': 3,
        }
        self.client.post(reverse('edit_product', kwargs={'product_id': product.pk}),
                         data=product_data)
        resp = self.client.get(reverse('products'))
        self.assertEqual(len(resp.context['product_list']), 10)

    def test_add_order(self):
        product = Product.objects.first()
        order_data = {
            'customer_mail': 'mail@mail.ru',
            'customer_first_name': 'John',
            'customer_middle_name': 'Wick',
            'customer_last_name': 'none',
            'customer_phone': '88005553535',
        }
        self.client.post(reverse('add_order', kwargs={'product_id': product.pk}),
                         data=order_data)
        orders_count = Order.objects.all().count()
        self.assertEqual(orders_count, 1)


class CompaniesListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_companies = 10
        for company_num in range(number_of_companies):
            Company.objects.create(name=company_num, user_id=company_num, description='default description')

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('companies_page'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('companies_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'companies.html')

    def test_lists_all_products(self):
        resp = self.client.get(reverse('companies_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['companies']), 10)

    def test_add_company(self):
        user = User.objects.create_user(username='username',
                                        email='user_mail',
                                        password='user_password')
        self.client.force_login(user)
        company_data = {
            'company_name': 'company_name',
            'company_description': 'company_description',
        }
        self.client.post(reverse('add_company'),
                         data=company_data)
        resp = self.client.get(reverse('companies_page'))
        self.assertEqual(len(resp.context['companies']), 11)


class UserPageAndMainPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username',
                                        email='user_mail',
                                        password='user_password')
        number_of_companies = 10
        for company_num in range(number_of_companies):
            Company.objects.create(name=company_num, user_id=user.id, description='default description')
        number_of_products = 10
        category = Category.objects.create(name='category')
        company = Company.objects.first()
        for product_num in range(number_of_products):
            Product.objects.create(company_id=company,
                                   category_id=category,
                                   name=product_num,
                                   percentage=13,
                                   period=3)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('user_page'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('user_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user_page.html')
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_lists_all_products_and_companies(self):
        self.client.force_login(User.objects.first())
        resp = self.client.get(reverse('user_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['companies']), 10)
        self.assertEqual(len(resp.context['products']), 10)
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['companies']), 10)
        self.assertEqual(len(resp.context['products']), 10)
