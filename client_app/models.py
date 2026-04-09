from django.db import models
from django.contrib.auth.models import User
from app.models import Domain, Client
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=250)
    password = models.CharField(max_length=128)
    
    email_id = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15)
    
    is_verified = models.BooleanField(default=False)
    
    client = models.ForeignKey(
        'app.Client',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    class Meta:
        db_table = "employee"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class TenantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "tenant_details"
        
        

class EmployeeSession(models.Model):
    tenant          = models.ForeignKey(
        'app.Client',
        on_delete=models.CASCADE,
        related_name='employee_sessions'
    )
    employee        = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    logged_in_time  = models.DateTimeField(default=timezone.now)
    logged_out_time = models.DateTimeField(null=True, blank=True)
    duration        = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in seconds")
    ip_address      = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "employee_session"

    def __str__(self):
        return f"{self.employee.name} | {self.logged_in_time}"

    def close_session(self):
        """Call this on logout to fill logged_out_time and duration."""
        self.logged_out_time = timezone.now()
        delta = self.logged_out_time - self.logged_in_time
        self.duration = int(delta.total_seconds())
        self.save()