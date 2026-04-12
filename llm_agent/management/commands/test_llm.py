from django.core.management.base import BaseCommand
from llm_agent.model_loader import ask_llm
from llm_agent.db_tools import (
    get_all_clients,
    get_client_by_name,
    get_employees_by_client,
    get_employee_detail,
)


class Command(BaseCommand):

    help = "Test LLM with real database data"

    def handle(self, *args, **kwargs):

        history = []

        print("\n=============================")
        print("   LLM + DATABASE TEST")
        print("=============================")
        print("1. Employee Details")
        print("2. List All Clients")
        print("3. List Employees of a Client")
        print("=============================")

        choice = input("Enter choice (1/2/3): ").strip()


        # ─────────────────────────────────────
        # CHOICE 1 — Employee Details
        # ─────────────────────────────────────
        if choice == "1":

            # Step 1 — fetch clients from DB
            clients      = get_all_clients()
            client_names = ", ".join([c["name"] for c in clients])

            print(f"\n[DB] Clients found: {client_names}")
            client_input = input("Enter client name: ").strip()

            # Step 2 — fetch employees from DB
            client = get_client_by_name(client_input)

            if not client:
                print(f"[DB] Client '{client_input}' not found.")
                return

            employees  = get_employees_by_client(client.schema_name)
            emp_list   = "\n".join([
                f"  - {e['name']} (ID: {e['id']}, Email: {e['email_id']}, Phone: {e['mobile_no']})"
                for e in employees
            ])

            print(f"\n[DB] Employees under '{client.name}':\n{emp_list}")
            emp_input = input("\nEnter employee name: ").strip()

            # Step 3 — fetch specific employee from DB
            employee = get_employee_detail(client.schema_name, emp_input)

            if not employee:
                print(f"[DB] Employee '{emp_input}' not found.")
                return

            # Step 4 — inject DB data into LLM history
            db_data = (
                f"[DB DATA]\n"
                f"Client   : {client.name}\n"
                f"Name     : {employee['name']}\n"
                f"Email    : {employee['email_id']}\n"
                f"Phone    : {employee['mobile_no']}\n"
                f"Verified : {'Yes' if employee['is_verified'] else 'No'}"
            )

            history.append({"role": "system", "content": db_data})
            history.append({"role": "user", "content": f"Show ONLY the fields present in the DB DATA above for employee {emp_input}. Do not add any extra fields."})

            print("\n[LLM] Generating response from DB data...")
            reply = ask_llm(history)
            print(f"\n[LLM REPLY]\n{reply}")


        # ─────────────────────────────────────
        # CHOICE 2 — List All Clients
        # ─────────────────────────────────────
        elif choice == "2":

            clients  = get_all_clients()
            db_data  = "[DB DATA]\nClients in system:\n"
            db_data += "\n".join([
                f"  - {c['name']} (schema: {c['schema_name']})"
                for c in clients
            ])

            history.append({"role": "system", "content": db_data})
            history.append({"role": "user",   "content": "List all clients"})

            print("\n[LLM] Generating response from DB data...")
            reply = ask_llm(history)
            print(f"\n[LLM REPLY]\n{reply}")


        # ─────────────────────────────────────
        # CHOICE 3 — Employees of a Client
        # ─────────────────────────────────────
        elif choice == "3":

            clients      = get_all_clients()
            client_names = ", ".join([c["name"] for c in clients])
            print(f"\n[DB] Available clients: {client_names}")

            client_input = input("Enter client name: ").strip()
            client       = get_client_by_name(client_input)

            if not client:
                print(f"[DB] Client '{client_input}' not found.")
                return

            employees = get_employees_by_client(client.schema_name)

            if not employees:
                print(f"[DB] No employees under '{client.name}'")
                return

            db_data  = f"[DB DATA]\nEmployees under client '{client.name}':\n"
            db_data += "\n".join([
                f"  - {e['name']} (Email: {e['email_id']}, Phone: {e['mobile_no']})"
                for e in employees
            ])

            history.append({"role": "system", "content": db_data})
            history.append({"role": "user",   "content": f"List employees of {client_input}"})

            print("\n[LLM] Generating response from DB data...")
            reply = ask_llm(history)
            print(f"\n[LLM REPLY]\n{reply}")

        else:
            print("Invalid choice.")