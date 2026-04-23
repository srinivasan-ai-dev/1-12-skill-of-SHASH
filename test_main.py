import traceback
import json
from scraper import get_all_data
from gemini_summarizer import generate_daily_brief

try:
    print("Scraping data...")
    data = get_all_data()
    print("Generating brief...")
    res = generate_daily_brief(data)
    print("RESULT:")
    print(res)
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
