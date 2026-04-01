from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Public index</h1>")

# # ====================================================> TESTING
# def check_tenant(request):
#     print(f"Tenant : {request.tenant.schema_name}")
#     return HttpResponse(
#         f"Tenant: {request.tenant.schema_name}, Host: {request.get_host()}"
#     )
# # ====================================================> TESTING