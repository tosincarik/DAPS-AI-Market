from fastapi import FastAPI, Request
from .crew import Analyser
from datetime import datetime

app = FastAPI(title="CrewAI Market Analysis API")

@app.get("/")
async def root():
    return {"message": "CrewAI Market Analysis API is running."}

@app.post("/run-analysis")
async def run_analysis(request: Request):
    data = await request.json()
    stock_symbol = data.get("stock_symbol", "AAPL")
    news_topic = data.get("news_topic", "Apple stock")

    inputs = {
        "stock_symbol": stock_symbol,
        "news_topic": news_topic,
        "current_year": str(datetime.now().year)
    }

    try:
        result = Analyser().crew().kickoff(inputs=inputs)
        return {"status": "success", "result": result.raw}
    except Exception as e:
        return {"status": "error", "message": str(e)}
