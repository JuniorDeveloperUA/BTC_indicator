api_key = '_____________________'
api_secret = '___________________'
import requests
import talib
import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
import time
import matplotlib.pyplot as plt
import json




sell_signal = False
buy_signal = False
text = ""

def plot():
# Get historical candlestick data from Binance
    client = Client(api_key, api_secret)
    sym = "BTCUSDT"
    interval= Client.KLINE_INTERVAL_1MINUTE
    length=200
    mult=3.0
    rsi_period=14
    rsi_high=60
    rsi_low=32
    
    klines = client.get_klines(symbol=sym, interval=interval, limit=length+1)
    # print(klines)
    klines_df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'num_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
    klines_df.drop(columns=['close_time', 'quote_asset_vol', 'num_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'], inplace=True)
    klines_df.set_index('timestamp', inplace=True)
    klines_df = klines_df.astype('float64')
    klines_df['timestamp'] = pd.to_datetime(klines_df['timestamp'], unit='ms')

    # RSI 14 ++
    rsi = talib.RSI(klines_df['close'], rsi_period)
    vrsi = rsi


    hlc3 = (klines_df['high'] + klines_df['low'] + klines_df['close']) / 3.0
    basis = talib.SUM(hlc3 * klines_df['volume'], timeperiod=200) / talib.SUM(klines_df['volume'], timeperiod=200)


    # tp = (klines_df['high'] + klines_df['low']+ klines_df['close']) / 3
    # vpc = tp * klines_df['volume']
    # vpc_sum = vpc.rolling(window=14).sum()
    # v_sum = klines_df['volume'].rolling(window=14).sum()
    # vwpc = vpc_sum / v_sum
    # vrsi = 100 - (100 / (1 + (vwpc / tp)))

    # def sma(x = klines_df['close'], y = 1):
    #     return np.convolve(x, np.ones(y)/y, mode='valid')
    # ma = sma()
    
    # MA 1 ++
    ma = klines_df['close'].rolling(window=1).mean()
    ma = pd.Series(ma)

    # print(ma)
    
    # basis = talib.WMA(klines_df['close'], length)
    dev = mult * talib.STDDEV(klines_df['close'], length)
    upper_1 = basis + (0.236 * dev)
    upper_2 = basis + (0.382 * dev)
    upper_3 = basis + (0.5 * dev)
    upper_4 = basis + (0.618 * dev)
    upper_5 = basis + (0.764 * dev)
    upper_6 = basis + (1 * dev)
    lower_1 = basis - (0.236 * dev)
    lower_2 = basis - (0.382 * dev)
    lower_3 = basis - (0.5 * dev)
    lower_4 = basis - (0.618 * dev)
    lower_5 = basis - (0.764 * dev)
    lower_6 = basis - (1 * dev)

    # print(upper_6)

    ### Buy
    if vrsi.iloc[-1] < rsi_low:
        ### BUY B
        if ((ma.iloc[-1] < basis.iloc[-1]) and (ma.iloc[-2] >= basis.iloc[-2])):
            text = f"🥶1m TF\n RSI{vrsi.iloc[-1]}\n✅BUY BASIS SIGNAL\nPrice: {klines_df['close'].iloc[-1]}"
            send_message(text)
        list = (lower_1, lower_2, lower_3, lower_4, lower_5, lower_6)
        for item in list:
            if ((ma.iloc[-1] < item.iloc[-1]) and (ma.iloc[-2] >= item.iloc[-2])):
                text = f"🥶1m TF Time to buy BTC\nBolinger bands signal\nPrice: {klines_df['close'].iloc[-1]}\nLast candle price: {klines_df['close'].iloc[-2]}"
                send_message(text)


    ### Sell
    if vrsi.iloc[-1] > rsi_high:
        list = (upper_6, upper_5, upper_4)
        for item in list:
            if (ma.iloc[-1] > upper_4.iloc[-1]) and (ma.iloc[-2] <= upper_4.iloc[-2]):
                text = "1m TF\nTime to sell"
                send_message(text)

    print("check1")
    # print(f"{vrsi.iloc[-1]} < {rsi_low} RSI")
    # print(f"{ma.iloc[-1]} < {lower_1.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_1.iloc[-2]}   {(ma.iloc[-1] < lower_1.iloc[-1]) and (ma.iloc[-2] >= lower_1.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_2.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_2.iloc[-2]}   {(ma.iloc[-1] < lower_2.iloc[-1]) and (ma.iloc[-2] >= lower_2.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_3.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_3.iloc[-2]}   {(ma.iloc[-1] < lower_3.iloc[-1]) and (ma.iloc[-2] >= lower_3.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_4.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_4.iloc[-2]}   {(ma.iloc[-1] < lower_4.iloc[-1]) and (ma.iloc[-2] >= lower_4.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_5.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_5.iloc[-2]}   {(ma.iloc[-1] < lower_5.iloc[-1]) and (ma.iloc[-2] >= lower_5.iloc[-2])}")    
    # print(f"{ma.iloc[-1]} < {lower_6.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_6.iloc[-2]}   {(ma.iloc[-1] < lower_6.iloc[-1]) and (ma.iloc[-2] >= lower_6.iloc[-2])}")    

def get_signal15():
# Get historical candlestick data from Binance
    client = Client(api_key, api_secret)
    sym = "BTCUSDT"
    interval= Client.KLINE_INTERVAL_15MINUTE
    length=200
    mult=3.0
    rsi_period=14
    rsi_high=60
    rsi_low=32
    
    klines = client.get_klines(symbol=sym, interval=interval, limit=length+1)
    # print(klines)
    klines_df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'num_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
    klines_df.drop(columns=['close_time', 'quote_asset_vol', 'num_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'], inplace=True)
    klines_df.set_index('timestamp', inplace=True)
    klines_df = klines_df.astype('float64')

    # RSI 14 ++
    rsi = talib.RSI(klines_df['close'], rsi_period)
    vrsi = rsi

    hlc3 = (klines_df['high'] + klines_df['low'] + klines_df['close']) / 3.0
    basis = talib.SUM(hlc3 * klines_df['volume'], timeperiod=200) / talib.SUM(klines_df['volume'], timeperiod=200)


    ap = hlc3
    esa = talib.EMA(ap, 10)
    d = talib.EMA(abs(ap - esa), 10)
    ci = (ap - esa) / (0.015 * d)
    tci = talib.EMA(ci, 21)

    wt1 = tci
    # wt2 = talib.EMA(wt1, 4)
    # print(wt1)
    # tp = (klines_df['high'] + klines_df['low']+ klines_df['close']) / 3
    # vpc = tp * klines_df['volume']
    # vpc_sum = vpc.rolling(window=14).sum()
    # v_sum = klines_df['volume'].rolling(window=14).sum()
    # vwpc = vpc_sum / v_sum
    # vrsi = 100 - (100 / (1 + (vwpc / tp)))

    # def sma(x = klines_df['close'], y = 1):
    #     return np.convolve(x, np.ones(y)/y, mode='valid')
    # ma = sma()
    
    # MA 1 ++
    ma = klines_df['close'].rolling(window=1).mean()
    ma = pd.Series(ma)

    # print(ma)
    
    # basis = talib.WMA(klines_df['close'], length)
    dev = mult * talib.STDDEV(klines_df['close'], length)
    upper_1 = basis + (0.236 * dev)
    upper_2 = basis + (0.382 * dev)
    upper_3 = basis + (0.5 * dev)
    upper_4 = basis + (0.618 * dev)
    upper_5 = basis + (0.764 * dev)
    upper_6 = basis + (1 * dev)
    lower_1 = basis - (0.236 * dev)
    lower_2 = basis - (0.382 * dev)
    lower_3 = basis - (0.5 * dev)
    lower_4 = basis - (0.618 * dev)
    lower_5 = basis - (0.764 * dev)
    lower_6 = basis - (1 * dev)

    # print(upper_6)

    ### Buy
    if vrsi.iloc[-1] < rsi_low:
        ### BUY B
        if ((ma.iloc[-1] < basis.iloc[-1]) and (ma.iloc[-2] >= basis.iloc[-2])):
            text = f"🫡15m TF\n RSI {vrsi.iloc[-1]} (Good <32)\nWT: {str(wt1.iloc[-1])} (Good <60)\n✅BUY BASIS SIGNAL\nPrice: {klines_df['close'].iloc[-1]}"
            send_message(text)
        list = (lower_1, lower_2, lower_3, lower_4, lower_5, lower_6)
        for item in list:
            if ((ma.iloc[-1] < item.iloc[-1]) and (ma.iloc[-2] >= item.iloc[-2])):
                text = f"🫡15m TF\nTime to buy BTC\nBolinger bands signal\nPrice: {klines_df['close'].iloc[-1]}\nLast candle price: {klines_df['close'].iloc[-2]}"
                send_message(text)


    ### Sell
    if vrsi.iloc[-1] > rsi_high:
        list = (upper_6, upper_5, upper_4)
        for item in list:
            if (ma.iloc[-1] > upper_4.iloc[-1]) and (ma.iloc[-2] <= upper_4.iloc[-2]):
                text = f"15m TF\nTime to sell\n RSI {vrsi.iloc[-1]} (Good >60)\nWT: {str(wt1.iloc[-1])} (Good >60)"
                send_message(text)

    # print("check15")
    # print(f"{vrsi.iloc[-1]} < {rsi_low} RSI")
    # print(f"{ma.iloc[-1]} < {lower_1.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_1.iloc[-2]}   {(ma.iloc[-1] < lower_1.iloc[-1]) and (ma.iloc[-2] >= lower_1.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_2.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_2.iloc[-2]}   {(ma.iloc[-1] < lower_2.iloc[-1]) and (ma.iloc[-2] >= lower_2.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_3.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_3.iloc[-2]}   {(ma.iloc[-1] < lower_3.iloc[-1]) and (ma.iloc[-2] >= lower_3.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_4.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_4.iloc[-2]}   {(ma.iloc[-1] < lower_4.iloc[-1]) and (ma.iloc[-2] >= lower_4.iloc[-2])}")
    # print(f"{ma.iloc[-1]} < {lower_5.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_5.iloc[-2]}   {(ma.iloc[-1] < lower_5.iloc[-1]) and (ma.iloc[-2] >= lower_5.iloc[-2])}")    
    # print(f"{ma.iloc[-1]} < {lower_6.iloc[-1]}) and ({ma.iloc[-2]} >= {lower_6.iloc[-2]}   {(ma.iloc[-1] < lower_6.iloc[-1]) and (ma.iloc[-2] >= lower_6.iloc[-2])}")    


def send_message(text):
    message = text
    token = "________________"
    chat_id = "_______________"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + str(message) 
    results = requests.get(url_req)
    time.sleep(20)

while True:
    try:
        # plot()
        get_signal15()
    except Exception as e:
        send_message(e)
