from django import forms

class EmployeeForm(forms.Form):
    name = forms.CharField(
        max_length=250, 
        label="Name", 
        widget=forms.TextInput(attrs={
            "placeholder": "Employee name"
        })
    )
    
    password = forms.CharField(
        max_length=128,
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Password"
        })
    )
    
    mobile_no = forms.CharField(
        max_length=15,
        label="Mobile Number",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter mobile number"
        })
    )
    
    email_id = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter email address"
        })
    )
    otp = forms.CharField(
        max_length=6,
        required=False,
        label="Enter OTP",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter 6-digit OTP"
        })
    )

class Tenant_login(forms.Form):
    employee_user = forms.CharField(
        max_length=250,
        label="Employee Username", 
        widget=forms.TextInput(attrs={
            "placeholder": "Employee Username"
        })
    )
    
    employee_password = forms.CharField(
        max_length=128,
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Password"
        })
    )