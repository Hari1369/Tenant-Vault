from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User


class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "sadmin_details"
        

class Client(TenantMixin):
    name = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    
        
class Domain(DomainMixin):
    pass


