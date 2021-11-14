import talib
from datetime import datetime

import ccxt
import numpy as np
import pandas as pd
import talib
import math
from indexing.decorators import timeit


@timeit
def get_all_coin_pairs(*derivative):
    base = {'binance': ccxt.binance, 'kucoin': ccxt.kucoin}
    if derivative[0] == 'future':
        exchange = base.get(derivative[1])(
            {'enableRateLimit': True, 'options': {'defaultType': 'future', }})
    else:
        exchange = ccxt.binance(
        {'enableRateLimit': True})
    load_markets = exchange.load_markets()
    all_coin_pairs = list(load_markets.keys())
    all_coin_pairs = [i for i in all_coin_pairs if len(i.split('/'))>1 and i.split('/')[1] == 'USDT']
    return all_coin_pairs

@timeit
def get_all_non_futures_pairs():
    exchange = ccxt.binance(
        {'enableRateLimit': True,})
    load_markets = exchange.load_markets()
    all_coin_pairs = list(load_markets.keys())
    return all_coin_pairs


def get_avg_tr(df, time_period):
    real = pd.Series()
    if not df.empty :
        real = talib.ATR(df['high'], df['low'], df['close'], timeperiod=time_period)
    return real


def get_basic_indicators(ind_type, candle_data_df, time_period):
    talib_api = {'EMA': talib.EMA, 'RSI': talib.RSI, 'WMA': talib.WMA}
    cl = candle_data_df['close']
    ind_vals = talib_api.get(ind_type.upper())(cl, timeperiod=time_period)
    ts = get_candle_timestamp(candle_data_df)
    return pd.concat([pd.Series(ts), ind_vals], axis=1)


def get_candle_data_with_timestamp(exchange, symbol, interval, limit, derivative):
    base = {'binance':ccxt.binance,'kucoin':ccxt.kucoin}
    try:
        if derivative =='future':
            exchange = base.get(exchange)(
                {'enableRateLimit': True, 'options': {'defaultType': 'future', }})
        else:
            exchange = ccxt.binance({'enableRateLimit': True})
        kline = exchange.fetch_ohlcv(symbol, interval, limit=int(limit))
        df = pd.DataFrame(np.array(kline), columns=['open_time', 'open', 'high', 'low', 'close', 'volume'],
                          dtype='float64')
        timestamps = df['open_time']
        ts = [datetime.fromtimestamp(
            int(i / 1000)).strftime('%Y-%m-%d %H:%M:%S') for i in timestamps]
        new_df = pd.concat(
            [pd.Series(ts).rename('open_timestamp'), df], axis=1)
        return new_df
    except Exception as e:
        print(e)


def get_candle_timestamp(df):
    timestamps = df['open_time']
    ts = [datetime.fromtimestamp(
        int(i / 1000)).strftime('%Y-%m-%d %H:%M:%S') for i in timestamps]
    return ts


def stochastic_crossover(df):
    hi = df['high']
    lo = df['low']
    cl = df['close']

    slowk, slowd = get_stochastic(hi, lo, cl, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3,
                                  slowd_matype=0)
    stch_mntm = slowk - slowd
    diff = pd.Series(['positive' if i >= 0 else 'Negative' for i in stch_mntm])
    ma_100 = get_ma(df, 100)
    stch_vs_ma_100 = pd.Series(
        ['bull' if df['close'][i] >= ma_100[1][i] else 'bear' for i in range(len(df))])
    df2 = pd.concat([df, pd.Series(stch_vs_ma_100).rename('trend'), diff.rename('momentum'), slowk.rename('slowk'),
                     slowd.rename('slowd')], axis=1)
    cross_over = ['crossover' if df2['momentum'][i - 1] !=
                  df2['momentum'][i] else 'None' for i in range(1, len(df))]
    cross_over.insert(0, 'start')
    final_df = pd.concat([df2, pd.Series(cross_over).rename('crossover'), pd.Series(ma_100[1]).rename('ma_100')],
                         axis=1)
    return final_df


def get_stochastic(hi, lo, cl, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3,
                   slowd_matype=0):
    slowk, slowd = talib.STOCH(hi, lo, cl, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3,
                               slowd_matype=0)
    return slowk, slowd


def get_ma(candle_data_df, time_period):
    cl = candle_data_df['close']
    ma = talib.MA(cl, timeperiod=time_period, matype=0)
    ts = get_candle_timestamp(candle_data_df)
    ma_with_time = pd.concat([pd.Series(ts), ma], axis=1)
    return ma_with_time


def update_candle_status(df):
    a = list(df['open'] - df['close'])
    b = []
    for i in range(len(a)):
        if i == 0:
            b.append(-1 if a[i] < 0 else 1)
        else:
            chn = -1 if a[i] < 0 else 1
            if b[i - 1] < 0 and chn < 0:
                b.append(b[i-1] -1)
            elif b[i - 1] > 0 and chn > 0:
                b.append(b[i-1] + 1)
            else:
                b.append(chn)
    b_updated = ['Red ' + str(i) if i > 0 else 'Green ' + str(i) for i in b]
    df['candle_status'] = pd.Series(b_updated)
    return df


def update_moving_averages(df, time_frame):
    if time_frame == '1w':
        df['ma_21'] = get_ma(df, 21)[1]
        df['diff_from_ma_21'] = (df['close'] - df['ma_21']) * 100 / df['close']
    else:
        df['ma_100'] = get_ma(df, 100)[1]
        df['diff_from_ma_100'] = (df['close'] - df['ma_100']) * 100 / df['close']
        df['ma_200'] = get_ma(df, 200)[1]
        df['diff_from_ma_200'] = (df['close'] - df['ma_200']) * 100 / df['close']
    return df
