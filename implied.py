import re
import math
from datetime import datetime, time, timedelta
from scipy.stats import norm
from scipy.optimize import fsolve
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# Option pricing parameters
underlyings = {'MAINIDX': 1848775, 'FINANCIALS': 1932270, 'ALLBANKS': 4379020, 'MIDCAPS':759205}

packet_input = """Publishing MarketData{symbol='MAINIDX20JUL2318100CE', LTP=56195, LTQ=100, totalTradedVolume=100, bestBid=55935, bestAsk=56735, bestBidQty=50, bestAskQty=100, openInterest=1850, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7473, prevClosePrice=7900, prevOpenInterest=9700}
Publishing MarketData{symbol='MAINIDX20JUL2318300CE', LTP=38505, LTQ=0, totalTradedVolume=0, bestBid=39105, bestAsk=39575, bestBidQty=100, bestAskQty=50, openInterest=27250, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7474, prevClosePrice=7950, prevOpenInterest=3700}
Publishing MarketData{symbol='MAINIDX13JUL2318150CE', LTP=45300, LTQ=0, totalTradedVolume=0, bestBid=48185, bestAsk=48585, bestBidQty=100, bestAskQty=50, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7475, prevClosePrice=7950, prevOpenInterest=6700}
Publishing MarketData{symbol='ALLBANKS06JUL2340900PE', LTP=550, LTQ=10250, totalTradedVolume=10250, bestBid=550, bestAsk=560, bestBidQty=2750, bestAskQty=1875, openInterest=43850, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7476, prevClosePrice=79700, prevOpenInterest=17075}
Publishing MarketData{symbol='MAINIDX06JUL2316750PE', LTP=130, LTQ=650, totalTradedVolume=650, bestBid=125, bestAsk=130, bestBidQty=5400, bestAskQty=6700, openInterest=5150, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7477, prevClosePrice=79700, prevOpenInterest=23800}
Publishing MarketData{symbol='ALLBANKS27JUL2342600PE', LTP=14240, LTQ=325, totalTradedVolume=325, bestBid=14090, bestAsk=14269, bestBidQty=50, bestAskQty=75, openInterest=32675, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7478, prevClosePrice=7975, prevOpenInterest=6675}
Publishing MarketData{symbol='ALLBANKS13JUL2341100PE', LTP=1935, LTQ=0, totalTradedVolume=0, bestBid=1270, bestAsk=1550, bestBidQty=50, bestAskQty=800, openInterest=1075, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7479, prevClosePrice=8000, prevOpenInterest=1700}
Publishing MarketData{symbol='FINANCIALS04JUL2318400CE', LTP=105565, LTQ=0, totalTradedVolume=0, bestBid=103759, bestAsk=105205, bestBidQty=40, bestAskQty=40, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7480, prevClosePrice=8000, prevOpenInterest=8200}
Publishing MarketData{symbol='ALLBANKS13JUL2342700PE', LTP=6720, LTQ=775, totalTradedVolume=775, bestBid=6300, bestAsk=6790, bestBidQty=25, bestAskQty=225, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7481, prevClosePrice=8025, prevOpenInterest=5575}
Publishing MarketData{symbol='MAINIDX26OCT2315000PE', LTP=2080, LTQ=0, totalTradedVolume=0, bestBid=2005, bestAsk=2010, bestBidQty=50, bestAskQty=50, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7482, prevClosePrice=8050, prevOpenInterest=100}
Publishing MarketData{symbol='ALLBANKS27JUL2342300PE', LTP=10885, LTQ=225, totalTradedVolume=225, bestBid=10815, bestAsk=10955, bestBidQty=50, bestAskQty=125, openInterest=60225, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7483, prevClosePrice=8050, prevOpenInterest=11300}
Publishing MarketData{symbol='MAINIDX27JUL2315000CE', LTP=353730, LTQ=0, totalTradedVolume=0, bestBid=360955, bestAsk=362965, bestBidQty=100, bestAskQty=550, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7484, prevClosePrice=8050, prevOpenInterest=7300}
Publishing MarketData{symbol='ALLBANKS13JUL2340500PE', LTP=1210, LTQ=0, totalTradedVolume=0, bestBid=960, bestAsk=1390, bestBidQty=25, bestAskQty=25, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7485, prevClosePrice=8075, prevOpenInterest=450}
Publishing MarketData{symbol='MAINIDX28SEP2317500PE', LTP=7750, LTQ=100, totalTradedVolume=100, bestBid=7640, bestAsk=7750, bestBidQty=100, bestAskQty=50, openInterest=183950, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7486, prevClosePrice=8100, prevOpenInterest=5250}
Publishing MarketData{symbol='MAINIDX20JUL2318700PE', LTP=21150, LTQ=0, totalTradedVolume=0, bestBid=19955, bestAsk=20535, bestBidQty=100, bestAskQty=50, openInterest=4700, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7487, prevClosePrice=8100, prevOpenInterest=7000}
Publishing MarketData{symbol='ALLBANKS27JUL2338900PE', LTP=1900, LTQ=0, totalTradedVolume=0, bestBid=1900, bestAsk=1900, bestBidQty=0, bestAskQty=0, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7488, prevClosePrice=8125, prevOpenInterest=25}
Publishing MarketData{symbol='MAINIDX06JUL2318300CE', LTP=30785, LTQ=46100, totalTradedVolume=46100, bestBid=30795, bestAsk=30870, bestBidQty=100, bestAskQty=200, openInterest=657050, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7489, prevClosePrice=81250, prevOpenInterest=72600}
Publishing MarketData{symbol='MAINIDX06JUL2319150CE', LTP=245, LTQ=91100, totalTradedVolume=91100, bestBid=245, bestAsk=250, bestBidQty=6450, bestAskQty=22650, openInterest=534350, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7490, prevClosePrice=815400, prevOpenInterest=126950}
Publishing MarketData{symbol='ALLBANKS13JUL2343000CE', LTP=120425, LTQ=925, totalTradedVolume=925, bestBid=121870, bestAsk=122359, bestBidQty=100, bestAskQty=100, openInterest=11625, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7491, prevClosePrice=8175, prevOpenInterest=4300}
Publishing MarketData{symbol='MAINIDX06JUL2318800PE', LTP=23025, LTQ=24100, totalTradedVolume=24100, bestBid=23040, bestAsk=23090, bestBidQty=600, bestAskQty=250, openInterest=309650, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7492, prevClosePrice=81900, prevOpenInterest=61050}
Publishing MarketData{symbol='MAINIDX28SEP2318500CE', LTP=57245, LTQ=50, totalTradedVolume=50, bestBid=57115, bestAsk=57835, bestBidQty=100, bestAskQty=50, openInterest=52450, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7493, prevClosePrice=8200, prevOpenInterest=5400}
Publishing MarketData{symbol='MAINIDX27JUL2318050CE', LTP=57200, LTQ=0, totalTradedVolume=0, bestBid=63620, bestAsk=64529, bestBidQty=100, bestAskQty=100, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7494, prevClosePrice=8200, prevOpenInterest=8450}
Publishing MarketData{symbol='ALLBANKS06JUL2340600PE', LTP=490, LTQ=3275, totalTradedVolume=3275, bestBid=490, bestAsk=500, bestBidQty=525, bestAskQty=425, openInterest=11725, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7495, prevClosePrice=82175, prevOpenInterest=8975}
Publishing MarketData{symbol='ALLBANKS06JUL2345900PE', LTP=205500, LTQ=0, totalTradedVolume=0, bestBid=178490, bestAsk=181490, bestBidQty=50, bestAskQty=50, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7496, prevClosePrice=8225, prevOpenInterest=7375}
Publishing MarketData{symbol='MAINIDX31AUG2318300PE', LTP=14900, LTQ=1800, totalTradedVolume=1800, bestBid=14819, bestAsk=14910, bestBidQty=100, bestAskQty=50, openInterest=238050, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7497, prevClosePrice=8250, prevOpenInterest=14900}
Publishing MarketData{symbol='MAINIDX27JUL2318150CE', LTP=50010, LTQ=0, totalTradedVolume=0, bestBid=55045, bestAsk=55885, bestBidQty=100, bestAskQty=100, openInterest=0, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7498, prevClosePrice=8250, prevOpenInterest=9600}
Publishing MarketData{symbol='ALLBANKS06JUL2346500CE', LTP=570, LTQ=59000, totalTradedVolume=59000, bestBid=565, bestAsk=570, bestBidQty=8375, bestAskQty=2800, openInterest=1503075, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7499, prevClosePrice=83125, prevOpenInterest=44675}
Publishing MarketData{symbol='ALLBANKS20JUL2344000PE', LTP=44290, LTQ=625, totalTradedVolume=625, bestBid=43505, bestAsk=44220, bestBidQty=25, bestAskQty=50, openInterest=7125, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7500, prevClosePrice=8325, prevOpenInterest=4125}
Publishing MarketData{symbol='ALLBANKS27JUL2343700CE', LTP=85430, LTQ=2625, totalTradedVolume=2625, bestBid=85055, bestAsk=85380, bestBidQty=50, bestAskQty=25, openInterest=70225, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7501, prevClosePrice=8350, prevOpenInterest=9900}
Publishing MarketData{symbol='FINANCIALS04JUL2320500CE', LTP=100, LTQ=72160, totalTradedVolume=72160, bestBid=95, bestAsk=100, bestBidQty=45360, bestAskQty=101800, openInterest=1917680, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7502, prevClosePrice=836240, prevOpenInterest=349200}
Publishing MarketData{symbol='MAINIDX06JUL2319000CE', LTP=509, LTQ=519950, totalTradedVolume=519950, bestBid=509, bestAsk=515, bestBidQty=100400, bestAskQty=28850, openInterest=4446900, timestamp=Mon Jul 03 22:19:54 IST 2023, sequence=7503, prevClosePrice=836850, prevOpenInterest=254450}
"""

risk_free_rate = 0.05  



def calculate_ttm(expiry_time):
    current_datetime = datetime.now()

    if current_datetime.time() > expiry_time:
        current_datetime += timedelta(days=1)

    

    packets = re.findall(r"Publishing MarketData{.*?}", packet_input)

    for packet in packets:
        packet_symbol_parts = re.findall(r"symbol='([A-Z]+)(\d{2}[A-Z]{3})(\d{2})", packet)
        if packet_symbol_parts:
            expiry_date = packet_symbol_parts[0][1] + packet_symbol_parts[0][2]  
            expiry_date = datetime.strptime(expiry_date, '%d%b%y').strftime('%Y-%m-%d')
            
        else:
            print("Symbol not found.")

    expiry_datetime = datetime.strptime(expiry_date + ' 15:30:00', '%Y-%m-%d %H:%M:%S')




    expiry_datetime = datetime.combine(current_datetime.date(), expiry_time)


    ttm = (expiry_datetime - current_datetime).total_seconds() / (365 * 24 * 60 * 60)
    return max(0, ttm)




def black_scholes(sigma, option_type, underlying_price, strike_price, ttm):
    d1 = (math.log(underlying_price / strike_price) + (risk_free_rate + 0.5 * sigma**2) * ttm) / (sigma * math.sqrt(ttm))
    d2 = d1 - sigma * math.sqrt(ttm)

    if option_type == 'CE':
        option_price = underlying_price * math.exp(-risk_free_rate * ttm) * norm.cdf(d1) - strike_price * math.exp(-risk_free_rate * ttm) * norm.cdf(d2)
    elif option_type == 'PE':
        option_price = strike_price * math.exp(-risk_free_rate * ttm) * norm.cdf(-d2) - underlying_price * math.exp(-risk_free_rate * ttm) * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Must be 'CE' (call) or 'PE' (put).")

    return option_price

def calculate_implied_volatility(option_type, observed_price, underlying_price, strike_price, ttm):
    if ttm < 0:
        return "0"

    def price_difference(sigma):
        return observed_price - black_scholes(sigma, option_type, underlying_price, strike_price, ttm)

    implied_volatility = fsolve(price_difference, 0.5)[0]
    if implied_volatility < 0:
        implied_volatility=0
    
    return implied_volatility

packets = re.findall(r"Publishing MarketData{.*?}", packet_input)

for packet in packets:
    symbol = re.search(r"symbol='(.*?)'", packet).group(1)
    observed_price = int(re.search(r"LTP=(\d+)", packet).group(1))
    
    underlying_price = None
    strike_price = None
    option_type = None
    
    for underlying in underlyings:
        if underlying in symbol:
            underlying_price = underlyings[underlying]
            break
    
    if underlying_price is None:
        continue
    
    if 'CE' in symbol:
        strike_price = int(re.search(r"(\d+)CE", symbol).group(1))
        option_type = 'CE'
    elif 'PE' in symbol:
        strike_price = int(re.search(r"(\d+)PE", symbol).group(1))
        option_type = 'PE'

    if strike_price is None or option_type is None:
        continue
    
    expiry_time = time(15, 30)  
    ttm = calculate_ttm(expiry_time)
    
    if option_type == 'PE':
        implied_volatility = calculate_implied_volatility(option_type, observed_price, underlying_price, strike_price, ttm)
        print("Symbol:", symbol)
        print("Implied Volatility (PE):", implied_volatility)
        print("---")



    else:
        option_type == 'CE'
        implied_volatility = calculate_implied_volatility(option_type, observed_price, underlying_price, strike_price, ttm)
        print("Symbol:", symbol)
        print("Implied Volatility (CE):", implied_volatility)
        print("---")




