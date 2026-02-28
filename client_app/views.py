from django.shortcuts import render, redirect
from django.http import HttpResponse
from client_app.models import Employee
# Create your views here.


def index(request):
    employee = Employee.objects.all()
    return render(request, "client_index.html", {"employees":employee})

def create_employee(request):
    if request.POST:
        name = request.POST.get("name")
        employee = Employee(name=name)
        employee.save()
    return redirect("client_index")