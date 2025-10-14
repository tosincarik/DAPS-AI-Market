import os
import requests

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_real_stock_data(symbol: str):
    """
    Fetches stock time series data from Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise Exception(f"Alpha Vantage API Error: {data.get('Note') or data.get('Error Message')}")
    
    return data["Time Series (Daily)"]


def get_real_news_sentiment(query: str):
    """
    Fetches latest news related to the topic from NewsAPI.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        raise Exception(f"NewsAPI Error: {data.get('message')}")
    
    articles = data.get("articles", [])
    return [
        {"title": a["title"], "description": a["description"], "publishedAt": a["publishedAt"]}
        for a in articles
    ]
