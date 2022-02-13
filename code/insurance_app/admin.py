from django.contrib import admin
from .models import Company, Category, Product, Order


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'description', ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'category_id', 'name', 'percentage', 'period', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'customer_middle_name', 'customer_first_name', 'customer_phone', 'customer_mail', ]


admin.site.register(Category)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)


