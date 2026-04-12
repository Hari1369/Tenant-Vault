# Request handler — replaces views.py entirely
# Handles HTTP, session, JSON in/out

import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .agent_core import process_message, reset_session


SESSION_KEY = "llm_agent_state"


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeAgentHandler(View):

    def post(self, request):
        """
        POST /llm/agent/
        Body: {"message": "Show employee data"}
        """
        try:
            body         = json.loads(request.body)
            user_message = body.get("message", "").strip()
        except (json.JSONDecodeError, KeyError):
            return JsonResponse(
                {"error": "Invalid JSON. Send: {\"message\": \"your text\"}"},
                status=400
            )

        if not user_message:
            return JsonResponse(
                {"error": "Message cannot be empty"},
                status=400
            )

        # Load agent state from Django session
        agent_state = request.session.get(SESSION_KEY, {})

        # Run the agent
        response, updated_state = process_message(user_message, agent_state)

        # Save updated state back to session
        request.session[SESSION_KEY] = updated_state
        request.session.modified = True

        return JsonResponse({
            "response"      : response,
            "current_stage" : updated_state.get("stage"),
            "client"        : updated_state.get("selected_client_name"),
            "employee"      : updated_state.get("selected_employee_name"),
        })


    def delete(self, request):
        """
        DELETE /llm/agent/
        Resets the entire conversation
        """
        request.session[SESSION_KEY] = reset_session({})
        request.session.modified = True

        return JsonResponse({"status": "Session reset successfully ✅"})


    def get(self, request):
        """
        GET /llm/agent/
        Returns current session state (for debugging)
        """
        agent_state = request.session.get(SESSION_KEY, {})

        return JsonResponse({
            "stage"    : agent_state.get("stage", "not started"),
            "client"   : agent_state.get("selected_client_name"),
            "employee" : agent_state.get("selected_employee_name"),
            "history_count": len(agent_state.get("history", [])),
        })