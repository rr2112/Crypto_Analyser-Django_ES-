import pandas as pd
import requests
import talib
from datetime import datetime

import ccxt
import numpy as np
import pandas as pd
import talib
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_waz_data():
    r = requests.get('https://api.wazirx.com/api/v2/market-status')
    data_dict = dict(r.json())['markets']

    df = pd.DataFrame()
    d = []
    d1 = {}
    usdt_price = 65
    for i in data_dict:
        if i['type'] == 'SPOT' and i['quoteMarket'] in ('inr', 'usdt', 'wrx', 'btc'):
            if i.get('baseMarket') == 'usdt':
                usdt_price = float(i['sell'])
            if not d1.get(i['baseMarket']):
                d1[i['baseMarket']] = {i['quoteMarket'] + 'sell': float(i['sell']),
                                       i['quoteMarket'] + 'buy': float(i['buy'])}
            else:
                d1[i['baseMarket']][i['quoteMarket'] + 'sell'] = float(i['sell'])
                d1[i['baseMarket']][i['quoteMarket'] + 'buy'] = float(i['buy'])
    return d1, usdt_price


def format_as_df(d1, usdt_price):
    coins_list = []
    all_coins = [i.upper() + '/USDT' for i in d1.keys()]
    binance_price = get_binance_price(all_coins)
    for i in d1:
        coin_pair = i.upper()+'/USDT'
        if len(d1[i]) > 2:
            temp = {'coin': i}
            temp.update(d1[i])
            coins_list.append(temp)

    df = pd.DataFrame(coins_list)
    df['usdt_price'] = usdt_price
    # df['converted_buy'] =
    df['inr-usdt-buy'] = df['inrbuy'] / usdt_price
    df['inr-usdt-sell'] = df['inrsell'] / usdt_price
    df['usdt-inr-buy'] = df['usdtbuy'] * usdt_price
    df['usdt-inr-sell'] = df['usdtsell'] * usdt_price
    df['buy-usdt-sell-inr'] = df['inr-usdt-buy'] - df['usdtsell']
    df['buy-inr-sell-usdt'] = df['usdt-inr-buy'] - df['inrsell']
    # df['bisu'] = (df['usdt-inr-buy']-df['inrsell'])*100/df['inrsell']
    df['bisu'] = df['buy-inr-sell-usdt'] * 100 / df['inrsell']

    return df

def get_binance_price(coins):
    exchange = ccxt.binance({'enableRateLimit': True})
    data = exchange.fetchTickers(coins)

if __name__ == '__main__':
    waz_data, usdt_price = get_waz_data()
    df = format_as_df(waz_data, usdt_price)
    print('****done****')
    print(usdt_price)
    df.to_excel("output.xlsx")
