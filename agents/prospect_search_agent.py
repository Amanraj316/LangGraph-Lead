# agents/prospect_search_agent.py

import time
from typing import List, Dict, Any

def run_prospect_search_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates searching for prospects using Clay and Apollo APIs.

    Args:
        state (Dict[str, Any]): The current state of the graph.
        config (Dict[str, Any]): The configuration for this specific step from workflow.json.

    Returns:
        Dict[str, Any]: An update to the state with the new leads.
    """
    print(f"\n--- EXECUTING PROSPECT SEARCH AGENT ---")
    print(f"Using ICP (Ideal Customer Profile): {config.get('icp')}")
    print("Searching for leads with Clay and Apollo APIs...")

    # Simulate API call latency
    time.sleep(2)

    # --- MOCK API RESPONSE ---
    # In a real scenario, you would make API calls to Clay/Apollo here.
    # For this exercise, we'll return a hardcoded list of leads.
    mock_leads = [
        {
            "company": "InnovateTech Inc.",
            "contact_name": "Alex Chen",
            "email": "alex.chen@innovatetech.com",
            "linkedin": "linkedin.com/in/alexcheninnovate",
            "signal": "recent_funding"
        },
        {
            "company": "DataSolutions LLC",
            "contact_name": "Brenda Rodriguez",
            "email": "brenda.r@datasolutions.com",
            "linkedin": "linkedin.com/in/brendarodriguezdata",
            "signal": "hiring_for_sales"
        }
    ]

    print(f"Found {len(mock_leads)} new leads.")
    print("--- PROSPECT SEARCH AGENT COMPLETED ---")

    # The key here MUST match the key in AgentState ('leads')
    return {"leads": mock_leads}