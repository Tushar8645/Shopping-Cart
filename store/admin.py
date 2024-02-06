from django.contrib import admin

from store.models import Product, Category, Customer, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'image']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone']
    readonly_fields = ['password']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity', 'price', 'status']
    readonly_fields = ['date', 'customer', 'product',
                       'quantity', 'price', 'address', 'phone']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
