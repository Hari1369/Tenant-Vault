# Tenant-Vault
Multi-Tenant Schema



<!-- TO MIGRATE -->
python manage.py migrate



<!-- ======================================== IMPORTANT ======================================== -->
>>> from app.models import Client, Domain
>>> tenant = Client(schema_name="public", name="public")
>>> tenant.save()
>>> domain = Domain(domain="localhost", tenant=tenant, is_primary=True)
>>> domain.save()
>>> tenant = Client(schema_name="quantumd", name="quantumd")
>>> tenant.save()
[1/1 (100%) standard:quantumd] === Starting migration
[1/1 (100%) standard:quantumd] Operations to perform:
[1/1 (100%) standard:quantumd]   Apply all migrations: admin, app, auth, contenttypes, sessions
[1/1 (100%) standard:quantumd] Running migrations:
[1/1 (100%) standard:quantumd]   Applying contenttypes.0001_initial...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0001_initial...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying admin.0001_initial...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying admin.0002_logentry_remove_auto_add...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying admin.0003_logentry_add_action_flag_choices...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying app.0001_initial...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying contenttypes.0002_remove_content_type_name...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0002_alter_permission_name_max_length...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0003_alter_user_email_max_length...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0004_alter_user_username_opts...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0005_alter_user_last_login_null...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0006_require_contenttypes_0002...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0007_alter_validators_add_error_messages...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0008_alter_user_username_max_length...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0009_alter_user_last_name_max_length...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0010_alter_group_name_max_length...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0011_update_proxy_permissions...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying auth.0012_alter_user_first_name_max_length...
[1/1 (100%) standard:quantumd]  OK
[1/1 (100%) standard:quantumd]   Applying sessions.0001_initial...
[1/1 (100%) standard:quantumd]  OK
>>> Domain = Domain(domain="quantumd.localhost", tenant=tenant, is_primary=True)
>>> Domain.save()
>>> 
<!-- ======================================== IMPORTANT ======================================== -->
