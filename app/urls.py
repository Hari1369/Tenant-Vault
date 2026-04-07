from django.contrib import admin
from django.urls import path
from app.views import index
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index),
    
    # # ====================================================> TESTING
    # path('', check_tenant),
    # # ====================================================> TESTING
]
