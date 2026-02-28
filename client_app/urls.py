from django.urls import path, include
from django.contrib import admin
from .views import index, create_employee

urlpatterns = [
    path('', index, name="client_index"),
    path('create_employee', create_employee, name="create_employee")
]
