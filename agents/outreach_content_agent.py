# agents/outreach_content_agent.py

from typing import Dict, Any
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_outreach_content_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates personalized outreach messages using an LLM.

    Args:
        state (Dict[str, Any]): The current state of the graph.
        config (Dict[str, Any]): The configuration for this specific step.

    Returns:
        Dict[str, Any]: An update to the state with the generated messages.
    """
    print("\n--- EXECUTING OUTREACH CONTENT AGENT ---")
    ranked_leads = state.get('ranked_leads', [])
    if not ranked_leads:
        print("No ranked leads to generate content for. Skipping.")
        return {}

    # Get API key from the tool's config
    cohere_api_key = config['tools'][0]['config']['api_key']
    if not cohere_api_key or cohere_api_key == "YOUR_COHERE_API_KEY":
        print("Cohere API key not found. Skipping.")
        return {"messages": []}

    # We'll only process the top 2 leads to save time/cost
    top_leads = ranked_leads[:2]
    print(f"Generating outreach messages for {len(top_leads)} top leads...")

    # Initialize the LLM
    llm = ChatCohere(model="command-a-03-2025", cohere_api_key=cohere_api_key)

    # Define the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Sales Development Representative (SDR). Your goal is to write a short, friendly, and highly personalized cold email. Use the provided context to make the email relevant to the recipient."),
        ("human", """
        Here is the context for the lead:
        - Contact Name: {contact_name}
        - Company: {company}
        - Role: {role}
        - Recent Signal: {signal}
        - Key Technologies they use: {technologies}

        Based on this, write a compelling but brief email body. Do not include a subject line or a greeting like "Hi {contact_name},". Start directly with the opening line.
        """)
    ])

    # Define the chain
    chain = prompt | llm | StrOutputParser()

    messages = []
    for lead in top_leads:
        print(f"  - Generating email for {lead['contact_name']} at {lead['company']}...")
        try:
            # Invoke the chain with the lead's data
            email_body = chain.invoke(lead)
            messages.append({
                "lead": lead,
                "email_body": email_body
            })
            print(f"  - Successfully generated email.")
        except Exception as e:
            print(f"  - Failed to generate email for {lead['contact_name']}: {e}")
            messages.append({
                "lead": lead,
                "email_body": f"Failed to generate content. Error: {e}"
            })

    print("--- OUTREACH CONTENT AGENT COMPLETED ---")
    return {"messages": messages}