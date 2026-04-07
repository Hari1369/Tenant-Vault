from django.contrib import admin
from .models import Employee, TenantUser

# Register your models here.
admin.site.register(Employee)
admin.site.register(TenantUser)