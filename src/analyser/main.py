#!/usr/bin/env python
import sys
from dotenv import load_dotenv
from datetime import datetime
from analyser.crew import Analyser

load_dotenv()

def run(stock_symbol="AAPL", news_topic=None):
    """
    Run the crew dynamically with stock_symbol and news_topic.
    """
    news_topic = news_topic or f"{stock_symbol} stock"

    inputs = {
        "stock_symbol": stock_symbol,
        "news_topic": news_topic,
        "current_year": str(datetime.now().year)
    }

    try:
        result = Analyser().crew(inputs=inputs).kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    # Optionally pass command line arguments: stock_symbol news_topic
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    run(symbol, topic)
