import os
import sys
import io
from dotenv import load_dotenv
from scraper import get_all_data
from gemini_summarizer import generate_daily_brief
from whatsapp_sender import send_whatsapp_message

# Set stdout to UTF-8 to prevent charmap errors on Windows when printing emojis
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("--- Starting AI Research & MAANG Hackathon Scraper ---")
    
    # 1. Load environment variables
    load_dotenv()
    print("Loaded environment variables.")
    
    # 2. Scrape data
    try:
        scraped_data = get_all_data()
        print("\nSuccessfully scraped data from all sources.")
    except Exception as e:
        print(f"Error during scraping: {e}")
        return

    # 3. Generate summary with Gemini
    try:
        print("\nGenerating AI summary tailored for you...")
        daily_brief = generate_daily_brief(scraped_data)
        print("AI summary generated successfully.")
    except Exception as e:
        print(f"Error during summarization: {e}")
        return

    # 4. Send via WhatsApp
    try:
        print("\nSending WhatsApp message...")
        success = send_whatsapp_message(daily_brief)
        if success:
            print("--- Run Complete! Check your WhatsApp ---")
        else:
            print("--- Run Finished, but WhatsApp sending failed. Please check credentials. ---")
            print("\nHere is the generated message you would have received:")
            print("-" * 50)
            print(daily_brief)
            print("-" * 50)
    except Exception as e:
        print(f"Error during WhatsApp sending: {e}")

if __name__ == "__main__":
    main()
