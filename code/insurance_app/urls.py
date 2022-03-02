from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.SignUpView.as_view(), name='register'),
    path('add_company', views.add_company, name='add_company'),
    path('user_page', views.user_page, name='user_page'),
    path('add_product/<int:company_id>', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>', views.edit_product, name='edit_product'),
    path('companies', views.companies_page, name='companies_page'),
    path('companies/<int:company_id>', views.company_page, name='company_page'),
    path('add_order/<int:product_id>', views.add_order, name='add_order'),
    path('search/', views.products_search, name='products_search'),
    path('products/', views.ProductsListView.as_view(), name='products'),
    path('products/<slug:pk>', views.ProductDetailView.as_view(), name='product')
]