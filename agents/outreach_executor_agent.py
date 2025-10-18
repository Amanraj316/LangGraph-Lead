# agents/outreach_executor_agent.py

import os
from typing import Dict, Any
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def run_outreach_executor_agent(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sends outreach messages via the SendGrid API.
    """
    print("\n--- EXECUTING OUTREACH EXECUTOR AGENT ---")
    messages = state.get('messages', [])
    if not messages:
        print("No messages to send. Skipping.")
        return {}

    # IMPORTANT: Get your verified sender email from .env or hardcode it
    # This MUST be an email you've verified in your SendGrid account.
    sender_email = os.getenv("SENDGRID_SENDER_EMAIL", "amanrajm5@gmail.com") 
    
    api_key = config['tools'][0]['config']['api_key']
    if not api_key or "YOUR_KEY_HERE" in api_key:
        print("SendGrid API key not found. Skipping.")
        return {"sent_status": []}

    sg = SendGridAPIClient(api_key)
    print(f"Attempting to send {len(messages)} emails via SendGrid...")
    
    sent_status = []
    for message in messages:
        lead = message.get('lead', {})
        email_address = lead.get('email', None)
        contact_name = lead.get('contact_name', 'Valued Prospect')
        email_body_text = message.get('email_body', '')

        if not email_address:
            continue

        # For the demo, you can redirect all emails to your own inbox
        # to avoid sending to the mock addresses.
        # recipient_email = "your-personal-email@gmail.com"
        recipient_email = "kaayu147@gmail.com"

        # Create the email message object
        mail_message = Mail(
            from_email=sender_email,
            to_emails=recipient_email,
            subject=f"A thought for {lead.get('company')}",
            html_content=f"Hi {contact_name},<br><br>{email_body_text.replace('\n', '<br>')}"
        )

        try:
            response = sg.send(mail_message)
            print(f"  - Email to {recipient_email} sent! Status Code: {response.status_code}")
            sent_status.append({
                "to": recipient_email,
                "status": "sent",
                "timestamp": datetime.datetime.now().isoformat(),
                "campaign_id": "campaign_XYZ_123"
            })
        except Exception as e:
            print(f"  - Failed to send email to {recipient_email}: {e}")
            sent_status.append({
                "to": recipient_email,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            })
            
    print("--- OUTREACH EXECUTOR AGENT COMPLETED ---")
    return {"sent_status": sent_status}