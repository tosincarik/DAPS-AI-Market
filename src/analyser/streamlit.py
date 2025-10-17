import streamlit as st
import requests

st.set_page_config(page_title="Market Analysis Dashboard", layout="wide")

st.title("📊 DAPS-AI Market Analysis")
st.write("Ask about any stock or topic, and get data-driven insights powered by CrewAI agents.")

# --- User input ---
user_query = st.text_input("Enter your question (e.g., 'What is Tesla looking like the past few weeks?')")

if st.button("Run Analysis"):
    if user_query:
        st.info(f"Analysing: **{user_query}** ...")

        try:
            response = requests.post(
                "http://127.0.0.1:8000/run-analysis",
                json={"stock_symbol": user_query, "news_topic": user_query},
                timeout=180
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    data = result.get("result", {})

                    # --- Final Recommendation ---
                    st.subheader("🟢 Final Recommendation")
                    st.write(f"**Recommendation:** {data.get('final_recommendation', 'N/A')}")
                    st.write(f"**Confidence:** {data.get('overall_confidence', 0):.2f}")

                    # --- Technical Indicators ---
                    st.markdown("### 📊 Technical Indicators")
                    tech = data.get("technical_indicators", {})
                    if tech:
                        st.write(f"**RSI:** {tech.get('RSI', 'N/A')}")
                        st.write(f"**MACD:** {tech.get('MACD', 'N/A')}")
                        ma = tech.get("moving_averages", {})
                        st.write(f"**Short-term MA:** {ma.get('short_term', 'N/A')}")
                        st.write(f"**Long-term MA:** {ma.get('long_term', 'N/A')}")

                    # --- Key Prices ---
                    st.markdown("### 💹 Key Prices")
                    prices = data.get("key_prices", {})
                    if prices:
                        st.write(f"**Latest Close:** {prices.get('latest_close', 'N/A')}")
                        st.write(f"**Recent High:** {prices.get('recent_high', 'N/A')}")
                        st.write(f"**Recent Low:** {prices.get('recent_low', 'N/A')}")

                    # --- Latest News ---
                    st.markdown("### 📰 Latest News Used in Analysis")
                    news_items = data.get("news_details", [])
                    if news_items:
                        for news in news_items:
                            st.markdown(f"**{news.get('title', 'No Title')}** ({news.get('date', 'No Date')})")
                            st.write(news.get('summary', 'No Summary'))
                            st.write(f"🧭 Sentiment Score: {news.get('sentiment_score', 'N/A')}")
                            st.divider()

                    # --- Justification ---
                    st.markdown("### 🧩 Justification Summary")
                    st.write(data.get("justification", "No justification provided."))

                else:
                    st.warning(f"No valid result returned: {result.get('message')}")
            else:
                st.error(f"Backend returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a query first.")
