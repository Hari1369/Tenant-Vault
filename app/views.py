from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import SuperAdmin

def index(request):
    return HttpResponse("<h1>Public index</h1>")

# def log_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             profile = user.SuperAdmin
#             if profile.role == 'super_admin':
#                 return redirect('admin_dashboard')
#             else:
#                 return redirect('dashboard')
#     else:


# # ====================================================> TESTING
# def check_tenant(request):
#     print(f"Tenant : {request.tenant.schema_name}")
#     return HttpResponse(
#         f"Tenant: {request.tenant.schema_name}, Host: {request.get_host()}"
#     )
# # ====================================================> TESTING


