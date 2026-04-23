import os
from twilio.rest import Client

def send_whatsapp_message(message_body):
    """
    Sends a WhatsApp message using Twilio's API.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_number = os.getenv("YOUR_WHATSAPP_NUMBER")
    
    if not all([account_sid, auth_token, from_number, to_number]):
        print("Error: Missing Twilio credentials or phone numbers in .env file.")
        print("Please ensure TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, and YOUR_WHATSAPP_NUMBER are set.")
        return False
        
    try:
        client = Client(account_sid, auth_token)
        
        # Twilio WhatsApp limit is 1600 characters.
        # We split the message into chunks if it's too long.
        max_length = 1500  # Conservative limit to account for byte-count of emojis
        chunks = [message_body[i:i+max_length] for i in range(0, len(message_body), max_length)]
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                chunk = f"(Part {i+1}/{len(chunks)})\n" + chunk
                
            message = client.messages.create(
                body=chunk,
                from_=from_number,
                to=to_number
            )
            print(f"WhatsApp chunk {i+1} sent! SID: {message.sid}")
            
        return True
    except Exception as e:
        print(f"Failed to send WhatsApp message. Error: {e}")
        return False

if __name__ == "__main__":
    # Test stub
    from dotenv import load_dotenv
    load_dotenv()
    send_whatsapp_message("🚀 Test message from your Daily Tech Opportunities bot!")
