from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.SignUpView.as_view(), name='register'),
    path('add_company', views.add_company, name='add_company'),
    path('user_page', views.user_page, name='user_page'),
    path('add_product/<int:company_id>', views.add_product, name='add_product'),
]