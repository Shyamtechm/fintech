import QuantLib as ql

def price_put_option(spot=450, strike=430, rate=0.05, vol=0.20):
    today = ql.Date.todaysDate()
    maturity = today + 180
    ql.Settings.instance().evaluationDate = today
    payoff = ql.PlainVanillaPayoff(ql.Option.Put, strike)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)
    riskFree = ql.FlatForward(today, rate, ql.Actual365Fixed())
    volCurve = ql.BlackConstantVol(today, ql.NullCalendar(), vol, ql.Actual365Fixed())
    process = ql.BlackScholesProcess(ql.QuoteHandle(ql.SimpleQuote(spot)), ql.YieldTermStructureHandle(riskFree), ql.BlackVolTermStructureHandle(volCurve))
    option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
    return option.NPV(), option.delta()
