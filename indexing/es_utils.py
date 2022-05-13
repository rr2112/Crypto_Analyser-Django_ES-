import math
import os
from datetime import datetime
from indexing.decorators import timeit
from elasticsearch import Elasticsearch


def es_connect():
    es = Elasticsearch([os.environ.get("es_second_host"),],http_auth=("elastic", os.environ.get("es_second_host_pass")), scheme="http",timeout=30,max_retries=10,retry_on_timeout=True,)
    return es


def update_time_frame(timeframe):
    """correction for index id :!caps not allowed"""
    if timeframe == "1m":
        timeframe = "1minute"
    elif timeframe == "1M":
        timeframe = "1month"
    return timeframe


def index_df(required_coins, timeframe):
    timeframe = update_time_frame(timeframe)
    length_of_df = len(required_coins)
    for i in range(length_of_df):
        process_df_rows(required_coins.iloc[i], timeframe)


def process_df_rows(df_row, timeframe):
    es = Elasticsearch(
        [
            os.environ.get("es_second_host"),
        ],
        http_auth=("elastic", os.environ.get("es_second_host_pass")),
        scheme="http",
        timeout=30,
        max_retries=10,
        retry_on_timeout=True,
    )
    # es = Elasticsearch([os.environ.get('es_trail_host'), ],
    #                    http_auth=('elastic', os.environ.get('es_trail_host_pass')), scheme="http", timeout=30,
    #                    max_retries=10, retry_on_timeout=True)

    try:
        df_row = df_row.fillna(0)
        index_unique_id = df_row["coin"] + relative_time(
            df_row["open_timestamp"], timeframe
        )
        data_body = {i: j for i, j in df_row.items()}
        data_body["open_timestamp_str"] = data_body["open_timestamp"]
        # timezone = pytz.timezone('Asia/Kolkata')
        # data_body['open_timestamp'] = timezone.localize(
        #     datetime.strptime(data_body['open_timestamp'], '%Y-%m-%d %H:%M:%S'))
        data_body["open_timestamp"] = datetime.strptime(
            data_body["open_timestamp"], "%Y-%m-%d %H:%M:%S"
        )
        del data_body["open_time"]
        if math.isinf(data_body["vol_change"]):
            del data_body["vol_change"]
        if math.isinf(data_body["prev_volume_change"]):
            del data_body["prev_volume_change"]
        result = es.index(
            index="atr_weightage_" + timeframe,
            doc_type="_doc",
            id=index_unique_id,
            body=data_body,
        )
    except Exception as e:
        print(e)


def relative_time(open_timestamp, timeframe):
    time_sensitivity = timeframe[::-1][0]
    time_stamp_for_index = {"m": 16, "e": 16, "h": 16, "d": 10, "w": 10, "M": 7}
    return open_timestamp[: time_stamp_for_index.get(time_sensitivity)]


@timeit
def index_total_df(df_o):
    index_data = []
    print("conn start", datetime.now())
    es = es_connect()
    print("conn end", datetime.now())
    print("length of dataframe", len(df_o))
    processed_records = 0
    temp_processed = 0
    for i in range(len(df_o)):
        df = df_o.iloc[i]
        try:
            df = df.fillna(0)
        except Exception as e:
            print(e)
        timeframe = df["timeframe"]
        u_id = df["coin"] + relative_time(df["open_timestamp"], df["timeframe"])
        data_body = {i: j for i, j in df.items()}
        data_body["open_timestamp_str"] = data_body["open_timestamp"]
        data_body["open_timestamp"] = datetime.strptime(
            data_body["open_timestamp"], "%Y-%m-%d %H:%M:%S"
        )
        del data_body["open_time"]
        if math.isinf(data_body["vol_change"]):
            del data_body["vol_change"]
        if math.isinf(data_body["prev_volume_change"]):
            del data_body["prev_volume_change"]
        index_data.append(({"index": {"_id": u_id}}))
        index_data.append(data_body)
        temp_processed += 1
        if temp_processed > 8000:
            print("8000 index start", datetime.now())
            es.bulk(
                index="atr_weightage_" + update_time_frame(timeframe), body=index_data
            )
            print("8000 index end", datetime.now())
            index_data = []
            processed_records += 8000
            pending_records = len(df_o) - processed_records
            print(
                f"processed_records:{processed_records}, pending_records:{pending_records}"
            )
            temp_processed = 0
    if index_data:
        print("end index start", datetime.now())
        es.bulk(index="atr_weightage_" + update_time_frame(timeframe), body=index_data)
        print("end index end", datetime.now())


def index_market_data(data, old_data):
    index_data = []
    # market_data = Market_Details.obj
    es = es_connect()
    for i in data:
        data[i]["old_rank"] = (
            old_data.get(data[i]["symbol"])
            if old_data.get(data[i]["symbol"])
            else data[i]["market_cap_rank"]
        )
        data[i]["rank_change"] = data[i]["old_rank"] - data[i]["market_cap_rank"]
        index_data.append(
            ({"index": {"_id": data[i]["symbol"] + str(data[i]["market_cap_rank"])}})
        )
        index_data.append(data[i])
    es.bulk(index="market_cap_data", body=index_data)
    print("market data indexed")
    return False
