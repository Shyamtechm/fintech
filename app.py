import streamlit as st
import ffn
import pandas as pd
import QuantLib as ql

st.set_page_config(page_title="Quant Portfolio Hedging System")

st.title("📈 Quantitative Portfolio Risk & Hedging System")

# ================= USER INPUT =================
symbols = st.text_input("Enter stock symbols (comma separated)", "AAPL,MSFT,TSLA,SPY")
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
strike = st.number_input("Put Option Strike (SPY)", 430.0)
vol = st.slider("Market Volatility", 0.10, 0.50, 0.20)

# =============== RUN BUTTON ==================
if st.button("Run Analysis"):

    tickers = symbols.replace(" ", "")
    prices = ffn.get(tickers, start=start_date)

    st.subheader("📊 Stock Prices")
    st.line_chart(prices)

    # ============ RETURNS ==================
    returns = prices.pct_change().dropna()

    # Portfolio return
    portfolio_returns = returns.mean(axis=1)

    # Volatility
    portfolio_vol = portfolio_returns.std() * (252 ** 0.5)

    st.metric("Annualized Volatility", f"{portfolio_vol*100:.2f}%")

    # ============ HEDGE DECISION ============
    if portfolio_vol > 0.25:
        hedge = "⚠ High Risk → Buy SPY Put Option"
    else:
        hedge = "✅ Risk Normal → No Hedge Required"

    st.subheader("🛡 Hedging Decision")
    st.success(hedge)

    # ============ OPTION PRICING (QuantLib) ============
    st.subheader("📉 Put Option Pricing (SPY)")

    spot = prices.mean(axis=1).iloc[-1]

    today = ql.Date.todaysDate()
    maturity = today + 180
    ql.Settings.instance().evaluationDate = today

    payoff = ql.PlainVanillaPayoff(ql.Option.Put, strike)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    riskFree = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    volCurve = ql.BlackConstantVol(today, ql.NullCalendar(), vol, ql.Actual365Fixed())

    process = ql.BlackScholesProcess(
        ql.QuoteHandle(ql.SimpleQuote(spot)),
        ql.YieldTermStructureHandle(riskFree),
        ql.BlackVolTermStructureHandle(volCurve)
    )

    option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

    st.write("Put Option Price:", round(option.NPV(),2))
    st.write("Option Delta:", round(option.delta(),3))
