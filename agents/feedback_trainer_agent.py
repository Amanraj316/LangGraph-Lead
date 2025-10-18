# agents/feedback_trainer_agent.py

import time
from typing import Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build

def run_feedback_trainer_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes campaign performance, suggests improvements, and writes them to a Google Sheet.
    """
    print("\n--- EXECUTING FEEDBACK TRAINER AGENT ---")
    responses = state.get('responses', [])
    ranked_leads = state.get('ranked_leads', [])

    if not responses or not ranked_leads:
        print("Missing data for analysis. Skipping.")
        return {}

    sheet_id = config['tools'][0]['config']['sheet_id']
    print(f"Analyzing {len(responses)} responses to suggest improvements...")

    # --- 1. Analyze Performance ---
    successful_lead = None
    for response in responses:
        if response.get("meeting_booked"):
            for lead in ranked_leads:
                if lead.get("email") == response.get("email"):
                    successful_lead = lead
                    break
        if successful_lead:
            break

    recommendations = []
    if successful_lead:
        recommendation_text = (
            f"Positive response from lead '{successful_lead['contact_name']}' "
            f"(Role: {successful_lead['role']}) from '{successful_lead['company']}'. "
            f"SUCCESS SIGNAL: This lead had the '{successful_lead['signal']}' signal. "
            f"RECOMMENDATION: Prioritize leads with this signal in the next run."
        )
        recommendations.append(recommendation_text)
    else:
        recommendations.append("No meetings booked. RECOMMENDATION: Consider tweaking email subject lines or the ICP.")

    # --- 2. Write to Google Sheets ---
    try:
        print(f"Writing {len(recommendations)} recommendations to Google Sheet ID: {sheet_id}...")

        # Define the scopes for the API
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'credentials.json'

        # Authenticate using the service account
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Prepare the row data to append
        # Each item in the outer list is a new row
        # Each item in the inner list is a cell in that row
        row_data = [
            [time.strftime("%Y-%m-%d %H:%M:%S"), recommendation] for recommendation in recommendations
        ]

        # Append the data to the sheet
        result = sheet.values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A1",  # Appends after the last row in this range
            valueInputOption="USER_ENTERED",
            body={"values": row_data}
        ).execute()

        print(f"Successfully wrote {result.get('updates').get('updatedRows')} row(s) to the sheet.")

    except FileNotFoundError:
        print("ERROR: `credentials.json` not found. Please ensure it's in the root directory.")
    except Exception as e:
        print(f"An error occurred while writing to Google Sheets: {e}")

    print("--- FEEDBACK TRAINER AGENT COMPLETED ---")
    return {"recommendations": recommendations}