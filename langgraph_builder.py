# langgraph_builder.py

import json
import os
from dotenv import load_dotenv
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
# langgraph_builder.py
from agents import (
    run_prospect_search_agent, 
    run_data_enrichment_agent, 
    run_scoring_agent,
    run_outreach_content_agent,
    run_outreach_executor_agent,
    run_response_tracker_agent,
    run_feedback_trainer_agent
)

# Define the state that will be passed between nodes
class AgentState(TypedDict):
    leads: List[Dict[str, Any]]
    enriched_leads: List[Dict[str, Any]]
    ranked_leads: List[Dict[str, Any]]
    messages: List[Dict[str, Any]]
    sent_status: List[Dict[str, Any]]
    responses: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]


class WorkflowBuilder:
    def __init__(self, workflow_path):
        """
        Initializes the WorkflowBuilder.
        
        Args:
            workflow_path (str): The path to the workflow.json file.
        """
        self.workflow_path = workflow_path
        self.workflow = None
        self.api_keys = {}
        # Map agent names from JSON to their actual Python functions
        self.agents = {
            "ProspectSearchAgent": run_prospect_search_agent,
            "DataEnrichmentAgent": run_data_enrichment_agent,
            "ScoringAgent": run_scoring_agent,
            "OutreachContentAgent": run_outreach_content_agent,
            "OutreachExecutorAgent": run_outreach_executor_agent,
            "ResponseTrackerAgent": run_response_tracker_agent,
            "FeedbackTrainerAgent": run_feedback_trainer_agent
            # We will add other agents here as we implement them
        }

    def _create_agent_node(self, step_config):
        """A factory function to create a node function for a given step."""
        agent_name = step_config['agent']
        agent_function = self.agents.get(agent_name)

        if not agent_function:
            # Return a default function if the agent is not implemented yet
            def placeholder_node(state: AgentState):
                print(f"\n--- SKIPPING {agent_name.upper()} (Not Implemented) ---")
                return {} # Return an empty dict to avoid overwriting state
            return placeholder_node

        def agent_node(state: AgentState):
            # Call the actual agent function with the current state and its specific config
            result = agent_function(state, step_config)
            return result

        return agent_node

    def load_environment_variables(self):
        """Loads API keys and other secrets from the .env file."""
        print("Loading environment variables...")
        load_dotenv()
        self.api_keys['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
        self.api_keys['CLAY_API_KEY'] = os.getenv('CLAY_API_KEY')
        self.api_keys['APOLLO_API_KEY'] = os.getenv('APOLLO_API_KEY')
        self.api_keys['CLEARBIT_KEY'] = os.getenv('CLEARBIT_KEY')
        self.api_keys['SENDGRID_API_KEY'] = os.getenv('SENDGRID_API_KEY')
        self.api_keys['SHEET_ID'] = os.getenv('SHEET_ID')
        print("Environment variables loaded.")

    def load_workflow(self):
        """Reads and validates the workflow.json file."""
        print(f"Loading workflow from {self.workflow_path}...")
        try:
            with open(self.workflow_path, 'r') as f:
                # We use a string replacement strategy for API keys
                workflow_str = f.read()
                for key, value in self.api_keys.items():
                    if value: # Only replace if the key exists in .env
                        workflow_str = workflow_str.replace(f'"{{{{{key}}}}}"', f'"{value}"')
                
                self.workflow = json.loads(workflow_str)
            print("Workflow loaded and API keys injected successfully.")
            return True
        except FileNotFoundError:
            print(f"Error: The file {self.workflow_path} was not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error: The file {self.workflow_path} is not a valid JSON.")
            return False

    def build(self):
        """Builds the LangGraph graph from the workflow definition."""
        if not self.workflow:
            print("Workflow not loaded. Cannot build the graph.")
            return None

        print("\nBuilding LangGraph from workflow...")
        workflow_graph = StateGraph(AgentState)

        # Dynamically create and add nodes to the graph
        for step in self.workflow.get("steps", []):
            step_id = step['id']
            print(f"  - Adding node: {step_id}")
            # Pass the entire step configuration to the node factory
            workflow_graph.add_node(step_id, self._create_agent_node(step))

        # Add edges to define the flow
        steps = [step['id'] for step in self.workflow.get("steps", [])]
        for i in range(len(steps) - 1):
            current_step = steps[i]
            next_step = steps[i+1]
            print(f"  - Adding edge: {current_step} -> {next_step}")
            workflow_graph.add_edge(current_step, next_step)
        
        # Set the entry and finish points of the graph
        workflow_graph.set_entry_point(steps[0])
        workflow_graph.add_edge(steps[-1], END)
        
        print("Graph built successfully.")
        return workflow_graph.compile()


# Main execution block
if __name__ == "__main__":
    builder = WorkflowBuilder('workflow.json')
    builder.load_environment_variables()
    if builder.load_workflow():
        app = builder.build()
        if app:
            # Define the initial state (it can be empty)
            initial_state = {}
            
            # Run the graph and get the final state
            final_state = app.invoke(initial_state)
            
            # Print the final state to see the results
            print("\n--- WORKFLOW COMPLETE ---")
            print("Final State:")
            print(json.dumps(final_state, indent=2))