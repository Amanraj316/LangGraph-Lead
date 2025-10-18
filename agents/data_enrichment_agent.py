# agents/data_enrichment_agent.py

import time
from typing import List, Dict, Any
import copy

def run_data_enrichment_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates enriching lead data using a service like Clearbit.

    Args:
        state (Dict[str, Any]): The current state of the graph.
        config (Dict[str, Any]): The configuration for this specific step.

    Returns:
        Dict[str, Any]: An update to the state with the enriched leads.
    """
    print("\n--- EXECUTING DATA ENRICHMENT AGENT ---")

    # Get the leads from the previous step
    leads = state.get('leads', [])
    if not leads:
        print("No leads to enrich. Skipping.")
        return {}

    print(f"Enriching {len(leads)} leads using Clearbit...")

    # Simulate API call latency
    time.sleep(2)

    enriched_leads = []
    # Deepcopy to avoid modifying the original list in the state
    leads_to_enrich = copy.deepcopy(leads)

    # --- MOCK ENRICHMENT LOGIC ---
    for lead in leads_to_enrich:
        if "Alex Chen" in lead.get("contact_name", ""):
            lead['role'] = 'VP of Engineering'
            lead['technologies'] = ['Python', 'AWS', 'React', 'Kubernetes']
        elif "Brenda Rodriguez" in lead.get("contact_name", ""):
            lead['role'] = 'Director of Sales'
            lead['technologies'] = ['Salesforce', 'HubSpot', 'Looker']

        enriched_leads.append(lead)

    print("Enrichment complete.")
    print("--- DATA ENRICHMENT AGENT COMPLETED ---")

    # The key here MUST match a key in AgentState ('enriched_leads')
    return {"enriched_leads": enriched_leads}