from django.contrib import admin
from .models import ExternalUser, Address, Company
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country')

admin.site.register(Address)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'title')

admin.site.register(Company)

class ExternalUserAdmin(admin.ModelAdmin):
    # 呢度要對應你 models.py 嘅欄位名
    list_display = ('first_name', 'last_name', 'email', 'username', 'role')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role', 'gender')

admin.site.register(ExternalUser)