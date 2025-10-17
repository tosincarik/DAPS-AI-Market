from fastapi import FastAPI, Request
from datetime import datetime
from .crew import Analyser
import json

app = FastAPI(title="CrewAI Market Analysis API")  # 👈 this MUST be before any @app decorator


@app.get("/")
async def root():
    return {"message": "CrewAI Market Analysis API is running."}



import json

@app.post("/run-analysis")
async def run_analysis(request: Request):
    data = await request.json()
    stock_symbol = data.get("stock_symbol", "AAPL")
    news_topic = data.get("news_topic", stock_symbol)

    inputs = {"stock_symbol": stock_symbol, "news_topic": news_topic}

    try:
        analyser = Analyser()
        crew_instance = analyser.crew()
        result = crew_instance.kickoff(inputs=inputs)  # kickoff with inputs

        if not result.raw:
            return {"status": "error", "message": "Crew returned no result"}

        # --- Parse raw output into dict if it is string ---
        if isinstance(result.raw, str):
            try:
                raw_data = json.loads(result.raw)
            except json.JSONDecodeError:
                return {"status": "error", "message": "Crew returned invalid JSON"}
        else:
            raw_data = result.raw

        # Build structured output including technical indicators and news
        structured_result = {
            "final_recommendation": raw_data.get("final_recommendation", "N/A"),
            "justification": raw_data.get("justification", ""),
            "overall_confidence": raw_data.get("overall_confidence", 0),
            "technical_indicators": raw_data.get("technical_indicators", {}),
            "key_prices": raw_data.get("key_prices", {}),
            "news_details": raw_data.get("news_details", [])
        }

        return {"status": "success", "result": structured_result}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
