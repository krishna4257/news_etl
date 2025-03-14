import requests
import json

API_KEY = "your_api_key"
URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

def extract_news():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data["articles"]  # Extract article data
    else:
        print("Error fetching news:", response.status_code)
        return []

# Fetch news
news_data = extract_news()
print(json.dumps(news_data[:2], indent=4)) 
