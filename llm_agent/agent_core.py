from .model_loader import ask_llm
from .db_tools import (
    get_all_clients,
    get_client_by_name,
    get_employees_by_client,
    get_employee_detail,
)

STAGE_START        = "start"
STAGE_ASK_CLIENT   = "ask_client"
STAGE_ASK_EMPLOYEE = "ask_employee"
STAGE_ASK_FIELDS   = "ask_fields"
STAGE_DONE         = "done"


def process_message(user_message, session):

    if "stage" not in session:
        session["stage"] = STAGE_START
    if "history" not in session:
        session["history"] = []

    history = session["history"]
    stage   = session["stage"]

    history.append({"role": "user", "content": user_message})


    # ════════════════════════════════════════
    # STAGE: START
    # ════════════════════════════════════════
    if stage == STAGE_START:
        clients      = get_all_clients()
        client_names = ", ".join([c["name"] for c in clients])

        # ✅ NO LLM — just return direct response
        response = f"Which client are you looking for?\nAvailable clients: {client_names}"
        session["stage"] = STAGE_ASK_CLIENT


    # ════════════════════════════════════════
    # STAGE: ASK_CLIENT
    # ════════════════════════════════════════
    elif stage == STAGE_ASK_CLIENT:
        client = get_client_by_name(user_message.strip())

        if not client:
            clients      = get_all_clients()
            client_names = ", ".join([c["name"] for c in clients])

            # ✅ NO LLM — direct response
            response = (
                f"❌ Client '{user_message}' not found.\n"
                f"Please choose from: {client_names}"
            )
            # Stay on same stage

        else:
            session["selected_client_schema"] = client.schema_name
            session["selected_client_name"]   = client.name

            employees = get_employees_by_client(client.schema_name)

            if not employees:
                # ✅ NO LLM — direct response
                response = f"No employees found under client '{client.name}'."
                session["stage"] = STAGE_DONE

            else:
                # ✅ NO LLM — build the list directly
                emp_lines = "\n".join([
                    f"  {i+1}. {e['name']} (ID: {e['id']})"
                    for i, e in enumerate(employees)
                ])
                response = (
                    f"Employees under '{client.name}':\n"
                    f"{emp_lines}\n\n"
                    f"Which employee do you want details for?"
                )
                session["stage"] = STAGE_ASK_EMPLOYEE


    # ════════════════════════════════════════
    # STAGE: ASK_EMPLOYEE
    # ════════════════════════════════════════
    elif stage == STAGE_ASK_EMPLOYEE:
        schema        = session.get("selected_client_schema")
        client_name   = session.get("selected_client_name")
        employee_name = user_message.strip()

        employee = get_employee_detail(schema, employee_name)

        if not employee:
            employees = get_employees_by_client(schema)
            emp_names = ", ".join([e["name"] for e in employees])

            # ✅ NO LLM — direct response
            response = (
                f"❌ Employee '{employee_name}' not found under '{client_name}'.\n"
                f"Available: {emp_names}"
            )
            # Stay on same stage

        else:
            session["selected_employee_name"] = employee["name"]
            session["selected_employee_data"] = employee

            # ✅ NO LLM — direct response
            response = (
                f"✅ Found '{employee['name']}'.\n"
                f"What details do you need?\n"
                f"Options: phone, email, verified status, all"
            )
            session["stage"] = STAGE_ASK_FIELDS


    # ════════════════════════════════════════
    # STAGE: ASK_FIELDS
    # ════════════════════════════════════════
    elif stage == STAGE_ASK_FIELDS:
        employee = session.get("selected_employee_data", {})
        user_req = user_message.lower()

        lines = []

        if any(k in user_req for k in ["phone", "mobile", "number", "contact"]):
            lines.append(f"  📞 Phone  : {employee.get('mobile_no', 'N/A')}")

        if any(k in user_req for k in ["email", "mail"]):
            lines.append(f"  📧 Email  : {employee.get('email_id', 'N/A')}")

        if any(k in user_req for k in ["verified", "verification", "status"]):
            v = "✅ Yes" if employee.get("is_verified") else "❌ No"
            lines.append(f"  🔍 Verified: {v}")

        if any(k in user_req for k in ["all", "everything", "full", "complete"]):
            v = "✅ Yes" if employee.get("is_verified") else "❌ No"
            lines = [
                f"  👤 Name   : {employee.get('name')}",
                f"  📧 Email  : {employee.get('email_id')}",
                f"  📞 Phone  : {employee.get('mobile_no')}",
                f"  🔍 Verified: {v}",
            ]

        if lines:
            details = "\n".join(lines)
            response = (
                f"Details for {employee.get('name')}:\n"
                f"{details}\n\n"
                f"Need anything else? (type 'another' to look up a different employee)"
            )
        else:
            response = (
                f"I didn't understand that.\n"
                f"Please ask for: phone, email, verified status, or all"
            )

        session["stage"] = STAGE_DONE


    # ════════════════════════════════════════
    # STAGE: DONE
    # ════════════════════════════════════════
    elif stage == STAGE_DONE:
        restart_keywords = ["another", "different", "other", "new", "start", "more", "yes"]

        if any(kw in user_message.lower() for kw in restart_keywords):
            session.pop("selected_client_schema", None)
            session.pop("selected_client_name",   None)
            session.pop("selected_employee_name", None)
            session.pop("selected_employee_data", None)

            clients      = get_all_clients()
            client_names = ", ".join([c["name"] for c in clients])

            response = f"Sure! Which client?\nAvailable: {client_names}"
            session["stage"] = STAGE_ASK_CLIENT

        else:
            response = "Session complete. Type 'another' to start a new query."

    else:
        response = "Something went wrong. Type 'another' to restart."


    history.append({"role": "assistant", "content": response})
    session["history"] = history

    return response, session


def reset_session():
    return {
        "stage"                  : STAGE_START,
        "history"                : [],
        "selected_client_schema" : None,
        "selected_client_name"   : None,
        "selected_employee_name" : None,
        "selected_employee_data" : None,
    }