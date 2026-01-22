from django.contrib import admin
from .models import ExternalCart,Product
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'user_id', 'total_products', 'discounted_total')

admin.site.register(ExternalCart)

class CartProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity')

admin.site.register(Product)
