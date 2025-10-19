# agents/data_enrichment_agent.py

import time
from typing import Dict, Any
import copy

def run_data_enrichment_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates enriching lead data to add specific roles and technologies.
    """
    print("\n--- EXECUTING DATA ENRICHMENT AGENT ---")
    
    leads = state.get('leads', [])
    if not leads:
        print("No leads to enrich. Skipping.")
        return {}

    print(f"Enriching {len(leads)} leads...")
    time.sleep(2)
    
    enriched_leads = []
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
    
    return {"enriched_leads": enriched_leads}