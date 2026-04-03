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
    