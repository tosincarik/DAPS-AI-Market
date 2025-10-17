
import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()  # Ensure environment variables are loaded

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_real_stock_data(symbol: str):
    """
    Fetch daily stock data from Alpha Vantage for the given symbol.
    Raises detailed errors if the API response is unexpected.
    """
    if not ALPHAVANTAGE_API_KEY:
        raise Exception("Alpha Vantage API key not found in environment variables.")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHAVANTAGE_API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(url, params=params)
    
    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"Failed to parse JSON from Alpha Vantage: {e}")

    # Debug: print the raw response to see what we got
    print(f"Alpha Vantage response for {symbol}:", data)

    if "Time Series (Daily)" not in data:
        error_msg = data.get("Note") or data.get("Error Message") or "Unexpected response structure"
        raise Exception(f"Alpha Vantage API Error: {error_msg}")

    return data["Time Series (Daily)"]



def get_real_news_sentiment(query: str):
    """
    Fetches recent news articles and runs lightweight sentiment analysis.
    Returns structured data with sentiment scores.
    """
    if not NEWS_API_KEY:
        raise Exception("News API key not found in environment variables.")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        raise Exception(f"NewsAPI Error: {data.get('message')}")

    articles = data.get("articles", [])
    processed_articles = []

    for article in articles:
        title = article.get("title", "Untitled")
        description = article.get("description") or ""
        content = article.get("content") or description
        source = article.get("source", {}).get("name", "Unknown Source")
        published_at = article.get("publishedAt", "")

        # --- Sentiment analysis ---
        sentiment = TextBlob(content).sentiment.polarity  # range: -1 to 1
        sentiment_score = round(sentiment, 3)
        sentiment_label = (
            "positive" if sentiment > 0.1 else
            "negative" if sentiment < -0.1 else
            "neutral"
        )

        processed_articles.append({
            "title": title,
            "summary": description[:200] + "...",
            "date": published_at.split("T")[0] if "T" in published_at else published_at,
            "source": source,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        })

    return processed_articles
