from django.contrib import admin
from .models import ExternalProduct,Tag,Review
# Register your models here.
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'stock', 'availability_status')
    search_fields = ('title', 'sku', 'brand')
    list_filter = ('category', 'brand', 'availability_status')
    inlines = [ReviewInline] 

admin.site.register(ExternalProduct)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Tag)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'rating', 'product', 'date')

admin.site.register(Review)
