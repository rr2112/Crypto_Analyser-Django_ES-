import math
import os
from datetime import datetime

from elasticsearch import Elasticsearch


def update_time_frame(timeframe):
    """ correction for index id :!caps not allowed"""
    if timeframe == '1m':
        timeframe = '1minute'
    elif timeframe == '1M':
        timeframe = '1month'
    return timeframe


# @timeit
def index_df(required_coins, timeframe):
    timeframe = update_time_frame(timeframe)
    length_of_df = len(required_coins)
    for i in range(length_of_df):
        process_df_rows(required_coins.iloc[i], timeframe)


def process_df_rows(df_row, timeframe):
    # es = Elasticsearch([os.environ.get('es_second_host'), ],
    #                    http_auth=('elastic', os.environ.get('es_second_host_pass')), scheme="http", timeout=30,
    #                    max_retries=10, retry_on_timeout=True)
    es = Elasticsearch([os.environ.get('es_trail_host'), ],
                       http_auth=('elastic', os.environ.get('es_trail_host_pass')), scheme="http", timeout=30,
                       max_retries=10, retry_on_timeout=True)

    try:
        df_row = df_row.fillna(0)
        index_unique_id = df_row['coin'] + \
                          relative_time(df_row['open_timestamp'], timeframe)
        data_body = {i: j for i, j in df_row.items()}
        data_body['open_timestamp_str'] = data_body['open_timestamp']
        # timezone = pytz.timezone('Asia/Kolkata')
        # data_body['open_timestamp'] = timezone.localize(
        #     datetime.strptime(data_body['open_timestamp'], '%Y-%m-%d %H:%M:%S'))
        data_body['open_timestamp'] = datetime.strptime(data_body['open_timestamp'], '%Y-%m-%d %H:%M:%S')
        del data_body['open_time']
        if math.isinf(data_body['vol_change']):
            del data_body['vol_change']
        if math.isinf(data_body['prev_volume_change']):
            del data_body['prev_volume_change']
        result = es.index(index='atr_weightage_' + timeframe,
                          doc_type='_doc', id=index_unique_id, body=data_body)
    except Exception as e:
        print(e)


def relative_time(open_timestamp, timeframe):
    time_sensitivity = timeframe[::-1][0]
    time_stamp_for_index = {'m': 16, 'e': 16,
                            'h': 16, 'd': 10, 'w': 10, 'M': 7}
    return open_timestamp[:time_stamp_for_index.get(time_sensitivity)]


