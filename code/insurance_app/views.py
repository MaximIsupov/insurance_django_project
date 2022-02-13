from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Company, Category, Product


class SignUpView(generic.CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = UserCreationForm
    success_message = "Регистрация прошла успешно"


def add_company(request):
    if request.method == 'GET':
        return render(request, 'add_company.html', {})
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
        return render(request, 'user_page.html', {})


def user_page(request):
    companies = Company.objects.filter(user_id=request.user.id)
    products = Product.objects.all()
    context = {'companies': companies,
               'products': products, }
    return render(request, 'user_page.html', context)


def index(request):
    return render(request, 'index.html', {})


