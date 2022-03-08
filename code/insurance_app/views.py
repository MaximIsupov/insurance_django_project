import os
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView
from .documents import ProductDocument
from elasticsearch_dsl import Q
from insurance_app.tasks import send_email_task
from .models import Company, Category, Product, Order
from pymongo import MongoClient


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
        user_id = product.company_id.user_id
        to_email = User.objects.get(id=user_id).email
        send_email_task(order, to_email)
        return render(request, 'index.html', context)


def products_search(request):
    search_keyword = request.GET['search_keyword']
    category_name = request.GET.get('category_name', 'not_selected')
    max_percentage = request.GET.get('percentage', 100)
    period_value = request.GET.get('period', 'not_selected')
    current_values = {'keyword': search_keyword,
                      'percentage': max_percentage,
                      'period': period_value}
    query_name = Q("multi_match",
                   query=search_keyword,
                   fields=[
                       'name',
                       'company_id.name'
                   ])
    query_category = Q("multi_match",
                       query=category_name,
                       fields=[
                           'category_id.name'
                       ])
    query_percentage = Q('range',
                         percentage={
                             'gte': 0,
                             'lte': max_percentage,
                         })
    query_period = Q('match',
                     period=period_value)
    s = ProductDocument.search()
    s = s.filter(query_name)
    if category_name and category_name != 'not_selected':
        s = s.filter(query_category)
        current_values['category'] = category_name
    s = s.filter(query_percentage)
    print(period_value)
    if period_value and period_value != 'not_selected':
        s = s.filter(query_period)
    categories = Category.objects.all()
    return render(request, 'search.html', {'qs': s,
                                           'values': current_values,
                                           'categories': categories,
                                           })


class ProductsListView(ListView):
    model = Product
    template_name = 'product_list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, *args, **kwargs):
        client = MongoClient(os.environ.get("MONGO_DB_HOST", "mongo"),
                             int(os.environ.get("MONGO_DB_PORT", 27017)))
        db = client[os.environ.get("MONGO_DB_NAME", "mongo_db")]
        collection = db['product_views']
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        views = 0
        if collection.find_one({'product_id': pk}):
            product_views = collection.find_one({'product_id': pk})
            print(product_views)
            product_views['views_count'] += 1
            print(product_views)
            views = product_views['views_count']
            collection.update_one({'product_id': pk},
                                  {"$set": {'views_count': views}})
        else:
            product_views = {'product_id': pk,
                             'views_count': 0}
            collection.insert_one(product_views)
        context['views'] = views
        return context


class AddCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse('index'))
