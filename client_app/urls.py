from django.urls import path, include
from django.contrib import admin
from .views import index, create_employee, tenant_log_in, index_page

urlpatterns = [
    path('', tenant_log_in, name="tenant_login"),
    path('client_dashboard', index_page, name="client_dashboard"),
    path('employee_add', index, name="client_index"),
    path('create_employee', create_employee, name="create_employee")
]
