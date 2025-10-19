# agents/prospect_search_agent.py

import time
from typing import Dict, Any

def run_prospect_search_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates searching for prospects to provide a reliable input for the workflow.
    """
    print("\n--- EXECUTING PROSPECT SEARCH AGENT ---")
    icp = config.get('icp')
    print(f"Using ICP (Ideal Customer Profile): {icp}")
    print("Searching for high-quality leads...")

    time.sleep(2)

    # --- ORIGINAL MOCK DATA ---
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

    return {"leads": mock_leads}