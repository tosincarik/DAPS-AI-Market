import requests

url = "http://127.0.0.1:8000/run-analysis"
payload = {"stock_symbol": "AAPL", "news_topic": "Apple stock"}

response = requests.post(url, json=payload)
print(response.json())
