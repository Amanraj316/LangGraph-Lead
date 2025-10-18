# agents/response_tracker_agent.py

import time
from typing import Dict, Any

def run_response_tracker_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates monitoring email responses and meeting bookings using Apollo API.

    Args:
        state (Dict[str, Any]): The current state of the graph.
        config (Dict[str, Any]): The configuration for this specific step.

    Returns:
        Dict[str, Any]: An update to the state with campaign responses.
    """
    print("\n--- EXECUTING RESPONSE TRACKER AGENT ---")
    sent_status = state.get('sent_status', [])
    if not sent_status:
        print("No sent emails to track. Skipping.")
        return {}

    campaign_id = sent_status[0].get("campaign_id") # Get ID from the first sent email
    print(f"Checking for responses for campaign: {campaign_id}...")

    # Simulate API call latency
    time.sleep(2)

    # --- MOCK API RESPONSE ---
    # In a real scenario, you'd poll the Apollo/SendGrid API.
    # Here, we'll simulate that one lead responded positively.
    mock_responses = [
        {
            "email": "alex.chen@innovatetech.com",
            "status": "replied",
            "reply_text": "This looks interesting. Do you have time to chat next week?",
            "meeting_booked": True
        },
        {
             "email": "brenda.r@datasolutions.com",
             "status": "opened",
             "reply_text": None,
             "meeting_booked": False
        }
    ]

    print(f"Found {len(mock_responses)} responses/events for the campaign.")
    print("--- RESPONSE TRACKER AGENT COMPLETED ---")

    return {"responses": mock_responses}