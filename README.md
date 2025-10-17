#📊 DAPS-AI Market Analysis Dashboard








Welcome to the DAPS-AI Market Analysis Dashboard, powered by CrewAI. This project is a multi-agent AI system designed to provide real-time, data-driven market insights for stocks and financial topics, combining technical analysis, news sentiment, and AI-powered consensus recommendations.

The system leverages live data from financial and news APIs, CrewAI agents, and a fully interactive Streamlit dashboard for visualization.

🚀 Features

Multi-agent analysis: Chart Analyst and News Analyst agents evaluate stocks.

Real-time data: Integrates live stock data and news from APIs.

DAP Protocol: Combines agent outputs via a mediator to generate a final recommendation.

Technical Insights: Displays key technical indicators such as RSI, MACD, and moving averages.

Key Prices: Shows latest close, recent highs, and recent lows.

News Summaries: Displays latest news items used for sentiment analysis.

Justification: Provides confidence-weighted reasoning for recommendations.

Interactive UI: Built with Streamlit for easy querying and visualization.

📦 Installation
Requirements

Python >= 3.10 and < 3.14

UV
 for dependency management

Steps

Clone the repository:


```
git clone https://github.com/yourusername/daps-ai-market.git
cd daps-ai-market

```

Install uv (if not already installed):

```
pip install uv
```

Install project dependencies:
```
crewai install

```

Configure API keys in a .env file at the project root:
```
ALPHAVANTAGE_API_KEY=your_alpha_vantage_api_key
NEWSAPI_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key
```

Note: Make sure your API keys are valid and have sufficient request limits.


Project Structure :
```
src/
 └─ analyser/
     ├─ crew.py               # Core CrewAI crew logic and agent definitions
     ├─ real_api.py           # Functions for fetching real-time stock & news data
     ├─ config/
     │   ├─ agents.yaml       # Agent configurations
     │   └─ tasks.yaml        # Task definitions
     ├─ app.py                # FastAPI backend for handling requests
     └─ streamlit.py          # Streamlit frontend dashboard
.env                         # Environment variables
```



⚡ Usage
1. Start the FastAPI Backend on one terminal

```
uvicorn src.analyser.app:app --reload
```

This starts the backend API on http://127.0.0.1:8000

2. Launch the Streamlit Dashboard

```
streamlit run src/analyser/streamlit.py
```

-Enter a stock symbol or company name (e.g., TSLA or Tesla).

-Ask a market-related question like:
-“What is Tesla looking like the past few weeks?”

-View the recommendation, confidence, technical indicators, key prices, news, and justification.



🛠 Technical Highlights

CrewAI Multi-Agent System

Chart Analyst: Technical stock analysis

News Analyst: News sentiment analysis

DAP Mediator: Weighted consensus on recommendation

Real API Integration

Live stock prices using Alpha Vantage

News sentiment analysis using NewsAPI

Streamlit Interactive UI

Dynamic query input (supports both ticker symbols and company names)

Interactive display of technical indicators, prices, news, and recommendations

🌐 Deployment

Backend API can be hosted on Render or any cloud provider that supports FastAPI.

Streamlit can be hosted separately for public dashboards.

Ensure environment variables are set in the hosting environment.

💡 Future Improvements

Add stock price charts and moving averages visualizations.

Include historical trends and predictions.

Expand agents to cover global market indices and commodities.

Add user authentication and custom watchlists.

📚 References

CrewAI Documentation

Alpha Vantage API

NewsAPI

Streamlit

🤝 Contribution

Contributions, suggestions, and bug reports are welcome! Open issues or submit pull requests.

📝 License

MIT License
