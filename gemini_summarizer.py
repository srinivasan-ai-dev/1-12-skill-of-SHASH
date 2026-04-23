import os
import json
from google import genai

def generate_daily_brief(scraped_data):
    """
    Uses Gemini to format and summarize the scraped data into an 
    actionable, highly-motivated WhatsApp message.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."
        
    client = genai.Client(api_key=api_key)
    
    # We use gemini-2.5-flash for fast, cheap (free tier), and excellent text generation
    model_name = 'gemini-2.5-flash'
    
    prompt = f"""
    You are an elite AI Career Architect for a 2nd-year CSE student at Anna University. 
    Their goal: AI Engineering at MAANG or high-paying Remote SWE jobs Abroad.
    Interests: Agents, Agentic AI, and Autonomous Systems.
    
    I have scraped the latest high-signal data:
    {json.dumps(scraped_data, indent=2)}
    
    Task:
    Create a 'Research-First' daily briefing. This is their competitive edge for MAANG.
    
    Constraints for the WhatsApp message:
    1. Greeting: High-energy, elite, and career-focused.
    2. *Research (The Next Big Thing)*: Select the 2 most impactful papers from the data. 
       - Explain WHY these papers are the 'Next Big Thing' for AI Agents/Autonomous Systems.
       - Use 2-3 sentences per paper. 
       - Provide the link clearly.
    3. *MAANG & High-Value Hackathons*: List the top 2-3 hackathons from the data. 
       - Highlight if it's from Google, Meta, NVIDIA, etc.
       - Explain why enrolling is a MUST for their career.
    4. *Agentic Tech News*: Mention 1-2 key news items about AI Agents or AGI.
    5. Tone: Motivating, punchy, and deeply technical yet skimmable.
    6. Formatting: Use WhatsApp markdown (*bold*, _italic_). Use emojis sparingly but effectively.
    7. CRITICAL: The message MUST be under 1500 characters. Be concise. Embedded links are key.
    8. Source: Mention if a paper is from ArXiv or Hugging Face.
    """
    
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return f"Could not generate AI summary. Raw data:\n{json.dumps(scraped_data, indent=2)}"

if __name__ == "__main__":
    # Test stub
    from dotenv import load_dotenv
    load_dotenv()
    test_data = {"papers": [{"title": "Test Paper", "summary": "Test Summary", "link": "http://test"}], "news": [], "internships": [], "hackathons": []}
    print(generate_daily_brief(test_data))
