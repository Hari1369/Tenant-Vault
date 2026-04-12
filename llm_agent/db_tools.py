from django_tenants.utils import schema_context
from app.models import Client
from client_app.models import Employee

def get_all_clients():
    clients = Client.objects.exclude(schema_name="public").values(
        "id", "name", "schema_name"
    )
    return list(clients)


def get_client_by_name(name):

    try:
        return Client.objects.exclude(schema_name="public").get(
            name__iexact=name
        )
    except Client.DoesNotExist:
        return None


def get_employees_by_client(schema_name):
    with schema_context(schema_name):
        employees = Employee.objects.all().values(
            "id", "name", "email_id", "mobile_no", "is_verified"
        )
        return list(employees)


def get_employee_detail(schema_name, employee_name):
    with schema_context(schema_name):
        try:
            emp = Employee.objects.get(name__iexact=employee_name)
            return {
                "id"         : emp.id,
                "name"       : emp.name,
                "email_id"   : emp.email_id,
                "mobile_no"  : emp.mobile_no,
                "is_verified": emp.is_verified,
            }
        except Employee.DoesNotExist:
            return None


def get_employee_by_id(schema_name, employee_id):
    with schema_context(schema_name):
        try:
            emp = Employee.objects.get(id=employee_id)
            return {
                "id"         : emp.id,
                "name"       : emp.name,
                "email_id"   : emp.email_id,
                "mobile_no"  : emp.mobile_no,
                "is_verified": emp.is_verified,
            }
        except Employee.DoesNotExist:
            return None