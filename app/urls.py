from django.contrib import admin
from django.urls import path
from app.views import index
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', index),

    # PUBLIC (shared app)
    path('', include("app.urls")),
    
    # # ====================================================> TESTING
    # path('', check_tenant),
    # # ====================================================> TESTING
]
