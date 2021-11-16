from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
# import qtpylib.indicators as qt
import talib
from django.core.management.base import BaseCommand

from indexing.decorators import timeit
from indexing.es_utils import index_df, index_total_df
from indexing.models import Market_Details
from indexing.utils import get_all_coin_pairs, get_candle_data_with_timestamp, get_avg_tr, get_basic_indicators, \
    stochastic_crossover, update_candle_status, update_moving_averages


class Command(BaseCommand):
    @timeit
    def handle(self, *args, **options):
        print("inside elastic index file")
        short_time_frames = ('1m',)  # '5m', '15m', '1h')
        long_time_frames = ('4h', '1d', '1w', '1M')
        all_coin_pairs = get_all_coin_pairs()
        all_time_frames = short_time_frames  # +long_time_frames
        result = main(all_coin_pairs, all_time_frames)
        print(result)


def scalping_report(coin_pair, time_frame, derivative,exchange='binance'):
    rsi_period = 5
    market_data = Market_Details.objects.filter(
        symbol=(coin_pair.rstrip('/USDT').rstrip('/BUSD')).lower()).values()
    market_details = dict(market_data[0]) if len(market_data) > 0 else {}
    df = pd.DataFrame()
    n_candles = {'1m': 30, '5m': 50, '1h': 40, '4h': 250, '1d': 250, '1w':250}
    try:
        df = get_candle_data_with_timestamp(
            exchange, coin_pair, time_frame, n_candles.get(time_frame,50), derivative)
        atr = get_avg_tr(df, 2)
        rsi = get_basic_indicators('RSI', df, rsi_period)
        df2 = pd.concat([df, atr.rename('atr')], axis=1)
        stochastic = stochastic_crossover(df2)
        df2['derivative'] = derivative
        df2['exchange'] = exchange
        df2['timeframe'] = time_frame
        df2['slowk'] = stochastic['slowk']
        df2['trend'] = stochastic['trend']
        df2['slowd'] = stochastic['slowd']
        df2['momentum'] = stochastic['momentum']
        df2 = update_moving_averages(df2,time_frame)
        df2['rsi-' + str(rsi_period)] = rsi[1]
        df2['coin'] = coin_pair
        df2['atr_weightage'] = (df2['atr'] / df2['open']) * 100
        df2['current_amplitude%(Hi-Op)'] = (df2['high'] -
                                            df2['open']) * 100 / df2['open']
        df2['open-close'] = (df2['close'] -
                             df2['open']) * 100 / df2['open']
        df2['prev-1_amplitude%'] = df2['current_amplitude%(Hi-Op)'].shift(
            periods=1)
        df2['prev-2_amplitude%'] = df2['current_amplitude%(Hi-Op)'].shift(
            periods=2)
        df2['prev-3_amplitude%'] = df2['current_amplitude%(Hi-Op)'].shift(
            periods=3)
        df2['market_cap_rank'] = market_details.get('market_cap_rank')
        df2['market_cap'] = market_details.get('market_cap')
        df2['vol_change'] = round(
            df2['volume'] / df2['volume'].shift(periods=1), 2)
        df2['prev_volume_change'] = df2['vol_change'].shift(periods=1)
        df2['OBV'] = talib.OBV(df['close'], df['volume'])
        # df2['VWAP'] = qt.vwap(df)
        # df2['diff_to_vwap'] = (df2['close']-df2['VWAP']) * 100 / df['close']
        df2 = update_candle_status(df2)
        if coin_pair.split('/')[0] in ('BTT','HBAR','ALGO','ONE','OCEAN','RSR','HOT','EGLD','FTT','FIL','TKO','TOMO','XRP','ETH','ATOM','DOGE','THETA','SOL','ADA','BNB','LTC','ENJ','MASK','WAVES','STEP','MITX','UBX','QRDO','POLC','POLX','BAX','WIN','VRA','TEL','HTR','BNB'):
            df2['to_invest'] = True
        temp_df = pd.DataFrame()
        # index_df(temp_df.append(df2), time_frame)
        return df2
    except Exception as e:
        print(e)


@timeit
def main(all_coin_pairs, all_time_frames,derivative,exchange):
    required_coins = pd.DataFrame()
    df_for_indexing = pd.DataFrame()
    no_of_workers = 60 if exchange == 'binance' else 5
    with ThreadPoolExecutor(max_workers=no_of_workers) as executor:
        future_to_f_detail = {executor.submit(scalping_report, id, timeframe, derivative,exchange): (id, timeframe, derivative, exchange) for timeframe in
                              all_time_frames for id in
                              all_coin_pairs}
        for future in as_completed(future_to_f_detail):
            _df = future.result()
            df_for_indexing = df_for_indexing.append(_df)
            required_coins = required_coins.append(_df[len(_df) - 1:])
        index_total_df(df_for_indexing)
        return required_coins

# @timeit
# def main_index_fn(market_details,all_coin_pairs):
#     short_time_frames = ('1m','5m', '15m', '1h')
#     long_time_frames = ('4h', '1d', '1w', '1M')
#     for timeframe in short_time_frames+long_time_frames:
#         # for timeframe in ('1d',):
#         required_coins, time_frame = main(timeframe,market_details,all_coin_pairs)
#         print("indexing finished for timeframe", timeframe)

#     # with ThreadPoolExecutor(max_workers=5) as exec:
#     #     result = {exec.submit(main, t):t for t in short_time_frames+long_time_frames}
#     #     for future in as_completed(result):
#     #         print("indexing finished for timeframe",result[future])
