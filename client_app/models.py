from django.db import models
from django.contrib.auth.models import User
from app.models import Domain, Client
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=250)
    password = models.CharField(max_length=128)
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
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "tenant_details"