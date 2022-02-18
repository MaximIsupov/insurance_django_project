import abc

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from .documents import ProductDocument
from elasticsearch_dsl import Q

from .models import Company, Category, Product, Order


class SignUpView(generic.CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = UserCreationForm
    success_message = "Регистрация прошла успешно"


def add_company(request):
    if request.method == 'GET':
        companies = Company.objects.all()[:5]
        products = Product.objects.all()[:5]
        context = {'companies': companies,
                   'products': products}
        return render(request, 'add_company.html', context)
    else:
        company_name = request.POST['company_name']
        company_description = request.POST['company_description']
        user_id = request.user.id
        company = Company(user_id=user_id,
                          name=company_name,
                          description=company_description)
        company.save()
        return render(request, 'index.html', {})


def add_product(request, company_id):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'add_product.html', {'categories': categories, })
    else:
        company = Company.objects.get(id=company_id)
        category = Category.objects.get(id=request.POST['category_id'])
        period = request.POST['period']
        percentage = request.POST['percentage']
        name = request.POST['product_name']
        product = Product(category_id=category,
                          company_id=company,
                          period=period,
                          percentage=percentage,
                          name=name)
        product.save()
        companies = Company.objects.filter(user_id=request.user.id)
        products = Product.objects.all()
        context = {'companies': companies,
                   'products': products, }
        return render(request, 'user_page.html', context)


def edit_product(request, product_id):
    if request.method == 'GET':
        categories = Category.objects.all()
        product = Product.objects.get(id=product_id)
        return render(request, 'add_product.html', {'categories': categories,
                                                    'product': product})
    else:
        product = Product.objects.get(id=product_id)
        category = Category.objects.get(id=request.POST['category_id'])
        period = request.POST['period']
        percentage = request.POST['percentage']
        name = request.POST['product_name']
        product.category_id = category
        product.period = period
        product.percentage = percentage
        product.name = name
        product.save()
        companies = Company.objects.filter(user_id=request.user.id)
        products = Product.objects.all()
        context = {'companies': companies,
                   'products': products, }
        return render(request, 'user_page.html', context)


def user_page(request):
    companies = Company.objects.filter(user_id=request.user.id)
    products = Product.objects.all()
    context = {'companies': companies,
               'products': products, }
    return render(request, 'user_page.html', context)


def index(request):
    companies = Company.objects.all()[:5]
    products = Product.objects.all()[:5]
    context = {'companies': companies,
               'products': products}
    return render(request, 'index.html', context)


def companies_page(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})


def company_page(request, company_id):
    company = Company.objects.get(id=company_id)
    products = Product.objects.filter(company_id=company)
    return render(request, 'company.html', {'products': products,
                                            'company': company})


def add_order(request, product_id):
    if request.method == 'GET':
        return render(request, 'add_order.html', {})
    else:
        product = Product.objects.get(id=product_id)
        customer_first_name = request.POST['customer_first_name']
        customer_middle_name = request.POST['customer_middle_name']
        customer_last_name = request.POST['customer_last_name']
        customer_phone = request.POST['customer_phone']
        customer_mail = request.POST['customer_mail']
        order = Order(customer_mail=customer_mail,
                      customer_first_name=customer_first_name,
                      customer_middle_name=customer_middle_name,
                      customer_last_name=customer_last_name,
                      customer_phone=int(customer_phone),
                      product_id=product)
        order.save()
        companies = Company.objects.all()[:5]
        products = Product.objects.all()[:5]
        context = {'companies': companies,
                   'products': products, }
        return render(request, 'index.html', context)


def products_search(request):
    document_class = ProductDocument
    search_keyword = request.POST('search_keyword')
    s = ProductDocument.search().filter("multi_match",
                                        query=search_keyword,
                                        fields=[
                                            'name',
                                            'company_id'
                                        ])
    return render(request, 'search.html', {'qs': s,
                                           'str': search_keyword})
