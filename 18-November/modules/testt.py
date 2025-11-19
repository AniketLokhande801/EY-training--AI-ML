# import yfinance as yf
# import matplotlib.pyplot as plt
# import io, base64
#
# def generate_chart(stock_symbol="TATAMOTORS.NS"):
#     # Fetch ~60 days to ensure 30 trading days
#     stock = yf.Ticker(stock_symbol)
#     hist = stock.history(period="60d")
#
#     if hist.empty:
#         print(f"No data found for {stock_symbol}")
#         return ""
#
#     # Take last 30 closes
#     closes = hist.tail(30)["Close"]
#     dates = closes.index.strftime("%Y-%m-%d").tolist()
#
#     # Plot chart
#     plt.style.use("seaborn-v0_8")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.plot(dates, closes.values, marker="o", linestyle="-", color="blue")
#     ax.set_title(f"{stock_symbol} - Last 30 Closing Prices")
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Closing Price (INR)")
#     fig.autofmt_xdate()
#
#     # Save to buffer
#     buf = io.BytesIO()
#     fig.savefig(buf, format="png")
#     plt.close(fig)
#     buf.seek(0)
#
#     # Encode to base64
#     chart_base64 = base64.b64encode(buf.read()).decode("utf-8")
#     return chart_base64
#
#
# if __name__ == "__main__":
#     symbol = "TATAMOTORS.NS"   # you can change this to test other stocks
#     chart_b64 = generate_chart(symbol)
#
#     if chart_b64:
#         print("✅ Chart generated successfully!")
#         print("Base64 string (first 200 chars):")
#         print(chart_b64[:200])  # print only first 200 chars for readability
#     else:
#         print("⚠️ No chart generated.")

import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODEL = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

st.title("📊 Advanced Portfolio Analysis (Prototype)")
st.write("Enter your stocks to analyze sector allocation using AI and get investment suggestions.")

# -------------------- FORM --------------------
with st.form("portfolio_form"):
    st.subheader("Enter Your Portfolio")

    stock_inputs = st.text_area(
        "Enter stock symbols and quantities (one per line, format: SYMBOL,QUANTITY)",
        placeholder="TCS,10\nRELIANCE,5\nHDFCBANK,8"
    )

    risk = st.selectbox("Select Your Risk Appetite", ["Low", "Moderate", "High"])

    submitted = st.form_submit_button("Analyze Portfolio")


# -------------------- PROCESS --------------------
if submitted:
    if not stock_inputs.strip():
        st.error("Please enter at least one stock.")
        st.stop()

    # Parse inputs
    parsed_stocks = []
    for line in stock_inputs.split("\n"):
        try:
            symbol, qty = line.split(",")
            parsed_stocks.append((symbol.strip().upper(), int(qty.strip())))
        except:
            st.error(f"Invalid format: {line}")
            st.stop()

    st.success("Portfolio Received! Classifying sectors using AI...")

    # -------------------- AI Sector Classification --------------------
    stock_details = []
    sector_data = {}

    for symbol, qty in parsed_stocks:
        prompt = f"""
        Identify the SECTOR for this Indian stock symbol: {symbol}.
        Only return the sector name (e.g., IT, Energy, Banking, FMCG, Pharma, Metals, Auto, Telecom).
        If unknown, guess based on the company name.
        """

        sector = MODEL.invoke(prompt).content.strip()

        stock_details.append((symbol, qty, sector))

        if sector not in sector_data:
            sector_data[sector] = 0
        sector_data[sector] += qty

    # -------------------- SHOW TABLE --------------------
    st.subheader("📌 Your Portfolio Breakdown (AI Sector Classification)")
    st.table(
        {
            "Stock": [s[0] for s in stock_details],
            "Quantity": [s[1] for s in stock_details],
            "Sector": [s[2] for s in stock_details],
        }
    )

    # -------------------- PIE CHART --------------------
    st.subheader("📊 Sector Allocation (AI-Detected)")
    fig, ax = plt.subplots()
    ax.pie(sector_data.values(), labels=sector_data.keys(), autopct="%1.1f%%")
    ax.axis("equal")
    st.pyplot(fig)

    # -------------------- BUTTON FOR MF + OTHER INVESTMENTS --------------------
    st.subheader("⚡ Want Diversification Recommendations?")
    if st.button("Suggest Other Investment Options"):
        st.info("Generating smart investment suggestions using AI...")

        mf_prompt = f"""
        The user's risk appetite is: {risk}.
        Their current portfolio sector distribution is: {sector_data}.

        Based on Indian market data:
        - Recommend top 3 mutual funds with 1-year returns.
        - Suggest allocation to Gold Bonds (SGB), REITs, and safer fixed-income if needed.
        - Adjust recommendations according to risk appetite.
        - Keep output very clear, structured, and professional.
        """

        response = MODEL.invoke(mf_prompt).content

        st.subheader("🎯 Recommended Investment Options")
        st.write(response)


