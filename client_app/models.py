from django.db import models
from django.contrib.auth.models import User
from app.models import Domain, Client

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=250)
    
    class Meta:
        db_table = "employee"
        

class TenantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "tenant_details"