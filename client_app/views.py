from django.shortcuts import render, redirect
from django.http import HttpResponse
from client_app.models import Employee
from .forms import EmployeeForm, Tenant_login
from django.contrib import messages

from .forms import Tenant_login
from client_app.models import Employee
from .utils import generate_otp, send_otp_email


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
            name            = form.cleaned_data["name"]
            password        = form.cleaned_data["password"]
            email_id        = form.cleaned_data["email_id"]
            phone_number    = form.cleaned_data["mobile_no"]
            otp_entered     = form.cleaned_data["otp"]

            # DEBUG
            print(f"NAME: {name}")
            print(f"OTP: {otp_entered}")

            if not otp_entered:
                otp = generate_otp()

                request.session['otp'] = otp
                request.session['user_data'] = {
                    "name": name,
                    "password": password,
                    "email_id": email_id,
                    "mobile_no": phone_number
                }

                send_otp_email(email_id, otp)

                messages.info(request, "OTP sent to your email")
                return render(request, "client_index.html", {"form": form})

            # STEP 2 → Verify OTP
            session_otp = request.session.get("otp")

            if otp_entered == session_otp:
                data = request.session.get("user_data")

                employee = Employee(
                    name=data["name"],
                    email_id=data["email_id"],
                    mobile_no=data["mobile_no"],  # ✅ FIXED
                    client=request.tenant
                )

                employee.set_password(data["password"])
                employee.save()

                request.session.flush()

                messages.success(request, "Employee added successfully!")
                return redirect("client_index")

            else:
                messages.error(request, "Invalid OTP")

    else:
        form = EmployeeForm()

    employees = Employee.objects.all()

    return render(request, "client_index.html", {
        "form": form,
        "employees": employees
    })
    
    
    
# ===================================================================================================
# ======================================================================> AJAX SUPPORT WITH NO RELOAD
# ===================================================================================================
 
# from django.shortcuts import render
# from django.http import JsonResponse

# from .forms import EmployeeForm
# from client_app.models import Employee

# from .services.otp_service import (
#     generate_otp, set_otp, get_otp,
#     is_otp_expired, can_resend_otp
# )
# from .services.email_service import send_otp_email


# def index(request):
#     form = EmployeeForm()
#     employees = Employee.objects.all()

#     return render(request, "client_index.html", {
#         "form": form,
#         "employees": employees
#     })


# def send_otp_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")

#         if not email:
#             return JsonResponse({"status": "error", "message": "Email required"})

#         if not can_resend_otp(email):
#             return JsonResponse({
#                 "status": "error",
#                 "message": "Wait 60 seconds before retry"
#             })

#         otp = generate_otp()
#         set_otp(email, otp)
#         send_otp_email(email, otp)

#         return JsonResponse({
#             "status": "success",
#             "message": "OTP sent successfully"
#         })

#     return JsonResponse({"status": "error"})


# def verify_otp_and_register(request):
#     if request.method == "POST":
#         form = EmployeeForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data["email_id"]
#             otp_entered = form.cleaned_data["otp"]

#             stored_otp = get_otp(email)

#             if is_otp_expired(email):
#                 return JsonResponse({
#                     "status": "error",
#                     "message": "OTP expired"
#                 })

#             if otp_entered != stored_otp:
#                 return JsonResponse({
#                     "status": "error",
#                     "message": "Invalid OTP"
#                 })

#             employee = Employee(
#                 name=form.cleaned_data["name"],
#                 email_id=email,
#                 mobile_no=form.cleaned_data["mobile_no"],
#                 client=request.tenant,
#                 is_verified=True
#             )

#             employee.set_password(form.cleaned_data["password"])
#             employee.save()

#             return JsonResponse({
#                 "status": "success",
#                 "message": "Registration successful"
#             })

#         return JsonResponse({
#             "status": "error",
#             "message": "Invalid form data"
#         })

#     return JsonResponse({"status": "error"})
# ===================================================================================================
# ======================================================================> AJAX SUPPORT WITH NO RELOAD
# ===================================================================================================