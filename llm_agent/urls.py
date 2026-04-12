from django.urls import path
from .handler import EmployeeAgentHandler

urlpatterns = [
    path("agent/", EmployeeAgentHandler.as_view(), name="employee-agent"),
]