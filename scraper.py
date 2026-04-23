import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import json

def fetch_research_papers():
    """Fetches the latest top AI research papers from ArXiv focusing on Agents and Autonomous Systems."""
    papers = []
    try:
        # Targeted query for Agents, Autonomous Systems, and Agentic AI
        query = '(all:agent+OR+all:autonomous+OR+all:agentic)+AND+(cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.RO)'
        url = f'http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=5'
        response = requests.get(url, timeout=15)
        root = ET.fromstring(response.text)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', namespace).text.strip().replace('\n', ' ')
            link = entry.find('atom:id', namespace).text.strip()
            papers.append({"title": title, "summary": summary, "link": link, "source": "ArXiv"})
            
    except Exception as e:
        print(f"Error fetching ArXiv: {e}")
    return papers[:3]

def fetch_hf_trending_papers():
    """Fetches trending papers from Hugging Face Daily Papers API."""
    papers = []
    try:
        url = "https://huggingface.co/api/daily_papers"
        response = requests.get(url, timeout=10)
        data = response.json()
        for item in data[:3]:
            paper = item.get('paper', {})
            title = paper.get('title', 'Unknown Title')
            id = paper.get('id')
            link = f"https://huggingface.co/papers/{id}" if id else ""
            summary = paper.get('summary', 'Click to read summary on Hugging Face.')
            papers.append({"title": title, "summary": summary, "link": link, "source": "Hugging Face"})
    except Exception as e:
        print(f"Error fetching Hugging Face: {e}")
    return papers

def fetch_tech_news():
    """Fetches tech news focusing on 'The Next Big Thing' (AI Agents/Autonomous)."""
    news = []
    try:
        # Searching Hacker News for 'Agent' or 'Autonomous'
        search_url = "https://hn.algolia.com/api/v1/search_by_date?query=AI+Agent&tags=story&hitsPerPage=3"
        response = requests.get(search_url, timeout=10).json()
        for hit in response.get('hits', []):
            news.append({"title": hit['title'], "link": hit['url'], "source": "HackerNews"})
    except Exception as e:
        print(f"Error fetching Tech News: {e}")
    return news

def fetch_hackathons():
    """Fetches MAANG and high-value AI hackathons using Devpost's JSON API."""
    hackathons = []
    keywords = ["Google", "Meta", "Microsoft", "NVIDIA", "OpenAI", "AWS", "Agentic"]
    
    for kw in keywords:
        try:
            # Using the JSON API endpoint found for better reliability
            url = f"https://devpost.com/api/hackathons?search={kw}&status[]=open&status[]=upcoming"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for hack in data.get('hackathons', []):
                    title = hack.get('title')
                    link = hack.get('url')
                    if title and link:
                        if not any(h['link'] == link for h in hackathons):
                            hackathons.append({"title": f"[{kw}] {title}", "link": link})
            if len(hackathons) >= 10: break # Cap total hackathons
        except Exception as e:
            print(f"Error fetching hackathons for {kw}: {e}")
            
    return hackathons[:5]

def get_all_data():
    """Aggregates all scraped data."""
    print("Scraping Research Papers (ArXiv & HF)...")
    papers = fetch_research_papers() + fetch_hf_trending_papers()
    print("Scraping Tech News (Focusing on Agents)...")
    news = fetch_tech_news()
    print("Scraping MAANG/High-Value Hackathons...")
    hackathons = fetch_hackathons()
    
    return {
        "papers": papers,
        "news": news,
        "hackathons": hackathons,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

if __name__ == "__main__":
    data = get_all_data()
    print(json.dumps(data, indent=2))
