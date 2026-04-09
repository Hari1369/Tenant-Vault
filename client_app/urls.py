from django.urls import path, include
from django.contrib import admin
from .views import index, create_employee, tenant_log_in, index_page, tenant_log_out

urlpatterns = [
    path('', tenant_log_in, name="tenant_login"),
    path('logout', tenant_log_out, name="tenant_logout"),
    path('client_dashboard', index_page, name="client_dashboard"),
    path('employee_add', index, name="client_index"),
    path('create_employee', create_employee, name="create_employee")
]



# ===================================================================================================
# ======================================================================> AJAX SUPPORT WITH NO RELOAD
# ===================================================================================================
# from django.urls import path
# from . import views
# urlpatterns = [
#     path("", views.index, name="client_index"),
#     path("send-otp/", views.send_otp_view, name="send_otp"),
#     path("verify/", views.verify_otp_and_register, name="verify_otp"),
# ]
# ===================================================================================================
# ======================================================================> AJAX SUPPORT WITH NO RELOAD
# ===================================================================================================