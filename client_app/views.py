from django.shortcuts import render, redirect
from django.http import HttpResponse
from client_app.models import Employee
from .forms import EmployeeForm
from django.contrib import messages

# Create your views here.
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
            
            # ✅ success message
            messages.success(request, "Employee added to system successfully!")

            return redirect("client_index")

    else:
        form = EmployeeForm()

    employees = Employee.objects.all()
    return render(request, "client_index.html", {
        "form": form,
        "employees": employees
    })
