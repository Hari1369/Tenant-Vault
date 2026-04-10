from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from client_app.models import Employee, EmployeeSession
from .forms import EmployeeForm, Tenant_login
from django.contrib import messages
from .utils import generate_otp, send_otp_email
from functools import wraps

import time


OTP_EXPIRY_SECONDS = 75

# ─────────────────────────────────────────
# Helper: get real IP (handles proxies too)
# ─────────────────────────────────────────
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

# ─────────────────────────────────────────
# Decorators
# ─────────────────────────────────────────
def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('tenant_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def logout_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_authenticated'):
            return redirect('client_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────
# Views
# ─────────────────────────────────────────
@logout_required_custom
def tenant_log_in(request):
    if request.method == "POST":
        form = Tenant_login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['employee_user']
            password = form.cleaned_data['employee_password']

            try:
                employee = Employee.objects.get(name=username)

                if employee.check_password(password):

                    # ── Django session ──────────────────────────────
                    request.session['employee_id']    = employee.id
                    request.session['employee_name']  = employee.name
                    request.session['is_authenticated'] = True

                    # ── Create EmployeeSession row ──────────────────
                    session_record = EmployeeSession.objects.create(
                        tenant     = request.tenant,
                        employee   = employee,
                        ip_address = get_client_ip(request)
                        # logged_in_time auto-set by default=timezone.now
                        # logged_out_time and duration are null until logout
                    )

                    # Store the DB session row ID so logout can find it
                    request.session['db_session_id'] = session_record.id

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


@login_required_custom
def tenant_log_out(request):
    db_session_id = request.session.get('db_session_id')

    if db_session_id:
        try:
            # ── Close the EmployeeSession row ───────────────────────
            session_record = EmployeeSession.objects.get(id=db_session_id)
            session_record.close_session()      # fills logout time + duration
        except EmployeeSession.DoesNotExist:
            pass

    request.session.flush()
    return redirect('tenant_login')


@login_required_custom
def index_page(request):
    return render(request, "client_dashboard.html")


@login_required_custom
def index(request):
    employee = Employee.objects.all()
    form = EmployeeForm()

    return render(request, "client_index.html", {
        "employees": employee,
        "form": form
    })


@require_POST
def send_otp(request):
    email_id = request.POST.get("email_id", "").strip()
    name     = request.POST.get("name", "").strip()
    password = request.POST.get("password", "").strip()
    mobile   = request.POST.get("mobile_no", "").strip()

    if not all([name, password, email_id, mobile]):
        return JsonResponse({"success": False, "error": "Please fill all fields before sending OTP."})

    # ── Check email uniqueness ────────────────────────────────────────
    if Employee.objects.filter(email_id=email_id).exists():
        return JsonResponse({"success": False, "error": "This email is already registered."})

    # ── Check phone uniqueness ────────────────────────────────────────
    if Employee.objects.filter(mobile_no=mobile).exists():
        return JsonResponse({"success": False, "error": "This phone number is already registered."})

    otp = generate_otp()
    request.session["otp"]           = otp
    request.session["otp_timestamp"] = time.time()
    request.session["user_data"]     = {
        "name":      name,
        "password":  password,
        "email_id":  email_id,
        "mobile_no": mobile,
    }

    send_otp_email(email_id, otp)
    return JsonResponse({"success": True, "message": "OTP sent to your email.", "expiry": OTP_EXPIRY_SECONDS})

def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            otp_entered = form.cleaned_data["otp"]

            if not otp_entered:
                form.add_error("otp", "Please enter the OTP sent to your email.")
                employees = Employee.objects.all()
                return render(request, "client_index.html", {"form": form, "employees": employees})

            session_otp       = request.session.get("otp")
            otp_timestamp     = request.session.get("otp_timestamp")

            # ── Expiry check ──────────────────────────────────────────────
            if not session_otp or not otp_timestamp:
                messages.error(request, "No OTP found. Please request a new one.")
            elif time.time() - otp_timestamp > OTP_EXPIRY_SECONDS:
                # Clean up expired OTP
                request.session.pop("otp", None)
                request.session.pop("otp_timestamp", None)
                request.session.pop("user_data", None)
                messages.error(request, "OTP has expired. Please request a new one.")
            elif otp_entered == session_otp:
                data = request.session.get("user_data", {})

                employee = Employee(
                    name      = data["name"],
                    email_id  = data["email_id"],
                    mobile_no = data["mobile_no"],
                    client    = request.tenant,
                )
                employee.set_password(data["password"])
                employee.save()

                request.session.pop("otp", None)
                request.session.pop("otp_timestamp", None)
                request.session.pop("user_data", None)

                messages.success(request, "Employee added successfully!")
                return redirect("client_index")
            else:
                messages.error(request, "Invalid OTP. Please try again.")

    else:
        form = EmployeeForm()

    employees = Employee.objects.all()
    return render(request, "client_index.html", {"form": form, "employees": employees})


#=====================================================================================================> UPDATED CODE
# def create_employee(request):
#     if request.method == "POST":
#         form = EmployeeForm(request.POST)

#         if form.is_valid():
#             name         = form.cleaned_data["name"]
#             password     = form.cleaned_data["password"]
#             email_id     = form.cleaned_data["email_id"]
#             phone_number = form.cleaned_data["mobile_no"]
#             otp_entered  = form.cleaned_data["otp"]

#             if not otp_entered:
#                 otp = generate_otp()
#                 request.session['otp'] = otp
#                 request.session['user_data'] = {
#                     "name": name,
#                     "password": password,
#                     "email_id": email_id,
#                     "mobile_no": phone_number
#                 }
#                 send_otp_email(email_id, otp)
#                 messages.info(request, "OTP sent to your email")
#                 return render(request, "client_index.html", {"form": form})

#             session_otp = request.session.get("otp")

#             if otp_entered == session_otp:
#                 data = request.session.get("user_data")

#                 employee = Employee(
#                     name      = data["name"],
#                     email_id  = data["email_id"],
#                     mobile_no = data["mobile_no"],
#                     client    = request.tenant
#                 )
#                 employee.set_password(data["password"])
#                 employee.save()

#                 # Only flush OTP-related keys, not the full login session
#                 request.session.pop('otp', None)
#                 request.session.pop('user_data', None)

#                 messages.success(request, "Employee added successfully!")
#                 return redirect("client_index")

#             else:
#                 messages.error(request, "Invalid OTP")

#     else:
#         form = EmployeeForm()

#     employees = Employee.objects.all()
#     return render(request, "client_index.html", {
#         "form": form,
#         "employees": employees
#     })
#=====================================================================================================> UPDATED CODE
    
    
    
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