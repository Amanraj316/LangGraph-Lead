# LangGraph-based Autonomous Prospect-to-Lead Workflow

This project is an end-to-end autonomous agent system designed to automate the B2B outbound lead generation process. It uses LangGraph to orchestrate a series of modular agents that handle everything from prospect discovery and enrichment to personalized outreach and performance analysis. The entire workflow is dynamically configured and controlled by a single `workflow.json` file.

## Features

-   **Dynamic Workflow:** The entire agent graph (nodes and edges) is built dynamically from the `workflow.json` configuration file, making it easy to reorder, add, or remove steps without changing the core logic.
-   **Modular Agents:** Each agent is a self-contained Python module located in the `/agents` directory, responsible for a single task (e.g., scoring, content generation).
-   **Live API Integrations:** The system integrates with several live services to perform real-world actions:
    -   **Cohere:** Generates personalized email content using an LLM.
    -   **SendGrid:** Sends the generated emails to prospects.
    -   **Google Sheets:** Logs feedback and recommendations for human review, creating a closed-loop system.
-   **Simulated Data Source:** To ensure a reliable and consistent demo, the initial `ProspectSearchAgent` and `DataEnrichmentAgent` are simulated to provide high-quality lead data, allowing the downstream live agents to function flawlessly.
-   **Stateful Execution:** The system maintains a shared state that is passed between agents, allowing each step to build upon the work of the previous one.

---

## Tech Stack

| Component         | Tool / Library         | Notes                                          |
| ----------------- | ---------------------- | ---------------------------------------------- |
| Agent Framework   | LangGraph & LangChain  | Core orchestration and agent framework         |
| LLM               | Cohere (Command R)     | For reasoning and personalized content generation |
| Email Delivery    | SendGrid API           | To send outreach emails                        |
| Config & Logging  | Google Sheets API      | For the feedback loop and human-in-the-loop approval |
| Environment       | Python, python-dotenv  | Core language and environment management       |

---

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.8+
-   A Google Cloud account with the Google Sheets API enabled.
-   Accounts for Cohere and SendGrid.

### 2. Clone the Repository

-git clone https://github.com/Amanraj316/LangGraph-Lead

### 3. Set Up the Environment
Create and activate a Python virtual environment to manage dependencies.


Create the virtual environment
python -m venv venv

Activate it
On Windows:
.\venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate

### 4. Install Dependencies
Install all the required Python libraries from the requirements.txt file.
pip install -r requirements.txt

### 5. Configure Environment Variables
This project requires several API keys and credentials to function.

A. Create the .env file: Create a file named .env in the root of the project directory and populate it with the following keys.
Cohere API Key for LLM content generation
COHERE_API_KEY="YOUR_COHERE_API_KEY"

SendGrid API Key and Verified Sender Email
SENDGRID_API_KEY="YOUR_SENDGRID_API_KEY"
SENDGRID_SENDER_EMAIL="your-verified-email@example.com"

Google Sheet ID for the feedback loop
From the URL: [https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit](https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit)
SHEET_ID="YOUR_GOOGLE_SHEET_ID"

B. Set up Google Credentials: This project uses a Service Account to write to Google Sheets.

Follow the official Google Cloud guide to create a service account.

During creation, grant the service account the "Editor" role.

Create a JSON key for the service account and download it.

Rename the downloaded file to credentials.json and place it in the root of the project directory.

Open your Google Sheet, click Share, and share it with the client_email found inside your credentials.json file, giving it Editor permissions.

Important: The credentials.json file is included in .gitignore and should never be committed to your repository.

### How to Run the Workflow
Once the setup is complete, you can run the entire end-to-end workflow with a single command:
python langgraph_builder.py

## Expected Outcome:
Terminal: You will see logs from each of the seven agents as they execute in sequence.

Email Inbox: You will receive two personalized emails sent via SendGrid to the address you configured.

Google Sheet: A new row containing a performance recommendation will be added to your specified Google Sheet.

### How to Extend or Modify
The system is designed to be modular and easy to extend.

Adding a New Agent
Create the Agent Logic: Create a new Python file in the /agents directory (e.g., new_agent.py). This file should contain a function that accepts state and config dictionaries and returns a dictionary with its results.

Import the Agent: Open agents/__init__.py and add an import statement for your new agent function.

Register the Agent: In langgraph_builder.py, import the new function and add it to the self.agents dictionary in the WorkflowBuilder class's __init__ method.
self.agents = {
    # ... other agents
    "NewAgentName": run_new_agent_function
}
4. Add to Workflow: Open workflow.json and add a new step object to the steps array for your new agent, ensuring the "agent" value matches the key you used in the dictionary above. Define its position in the sequence by placing it correctly in the array.
