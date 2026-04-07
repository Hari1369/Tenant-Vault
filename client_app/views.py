from django.shortcuts import render, redirect
from django.http import HttpResponse
from client_app.models import Employee
from .forms import EmployeeForm, Tenant_login
from django.contrib import messages

from django.shortcuts import render, redirect
from .forms import Tenant_login
from client_app.models import Employee

def index_page(request):
    print("Dashboard")
    return render(request, "client_dashboard.html")
    

def tenant_log_in(request):
    if request.method == "POST":
        print("Tenant:", request.tenant.schema_name)
        form = Tenant_login(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['employee_user']
            password = form.cleaned_data['employee_password']
            
            try:
                employee = Employee.objects.get(name=username)

                if employee.check_password(password):
                    return redirect('client_dashboard')
                else:
                    return render(request, "log_in.html", {
                        "form": form,
                        "error": "Invalid password"
                    })

            except Employee.DoesNotExist:
                return render(request, "log_in.html", {
                    "form": form,
                    "error": "User Not Found"
                })

    else:
        form = Tenant_login()
    return render(request, "log_in.html", {"form": form})


def index(request):
    employee = Employee.objects.all()
    form = EmployeeForm()

    return render(request, "client_index.html", {
        "employees": employee,
        "form": form
    })


def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            
            employee = Employee(
                name=name,
                client=request.tenant
            )
            employee.set_password(password)
            employee.save()
            
            messages.success(request, "Employee added to system successfully!")
            return redirect("client_index")

    else:
        form = EmployeeForm()

    employees = Employee.objects.all()
    return render(request, "client_index.html", {
        "form": form,
        "employees": employees
    })
