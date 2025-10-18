# agents/scoring_agent.py

import time
from typing import List, Dict, Any

def run_scoring_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scores enriched leads based on a simple scoring model.

    Args:
        state (Dict[str, Any]): The current state of the graph.
        config (Dict[str, Any]): The configuration for this specific step.

    Returns:
        Dict[str, Any]: An update to the state with the ranked leads.
    """
    print("\n--- EXECUTING SCORING AGENT ---")

    enriched_leads = state.get('enriched_leads', [])
    if not enriched_leads:
        print("No enriched leads to score. Skipping.")
        return {}

    print(f"Scoring {len(enriched_leads)} leads...")

    # Simulate processing time
    time.sleep(1)

    ranked_leads = []
    for lead in enriched_leads:
        score = 0
        # Score based on role
        if lead.get('role') in ['VP of Engineering', 'Director of Engineering']:
            score += 20
        elif lead.get('role') in ['Director of Sales']:
            score += 10

        # Score based on technologies
        tech_stack = lead.get('technologies', [])
        if 'AWS' in tech_stack:
            score += 10
        if 'Salesforce' in tech_stack:
            score += 5

        lead['score'] = score
        ranked_leads.append(lead)

    # Sort leads by score in descending order
    ranked_leads.sort(key=lambda x: x['score'], reverse=True)

    print("Lead scoring complete.")
    print("--- SCORING AGENT COMPLETED ---")

    return {"ranked_leads": ranked_leads}