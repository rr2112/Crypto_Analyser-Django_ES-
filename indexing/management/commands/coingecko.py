from concurrent.futures import ThreadPoolExecutor
import time

from pycoingecko import CoinGeckoAPI

from indexing.decorators import timeit

result = {}

def get_market_caps_per_page(page_required):
    global result
    cg = CoinGeckoAPI()
    markets = cg.get_coins_markets(vs_currency='usd', page=page_required)
    result.update({i['symbol'].upper(): {
        'id': i['id'], 'symbol': i['symbol'], 'name': i['name'], 'image': i['image'],
        'current_price': i['current_price'], 'market_cap': i['market_cap'], 'market_cap_rank': i['market_cap_rank'],
        'fully_diluted_valuation': i['fully_diluted_valuation'], 'total_volume': i['total_volume'],
        'high_24h': i['high_24h'], 'low_24h': i['low_24h'], 'price_change_24h': i['price_change_24h'],
        'price_change_percentage_24h': i['price_change_percentage_24h'],
        'market_cap_change_24h': i['market_cap_change_24h'],
        'market_cap_change_percentage_24h': i['market_cap_change_percentage_24h'],
        'circulating_supply': i['circulating_supply'], 'total_supply': i['total_supply'], 'max_supply': i['max_supply'],
        'ath': i['ath'], 'ath_change_percentage': i['ath_change_percentage'], 'ath_date': i['ath_date'],
        'atl': i['atl'], 'atl_change_percentage': i['atl_change_percentage'], 'atl_date': i['atl_date'],
        'roi': i['roi'], 'last_updated': i['last_updated'],
    } for i in
        markets})

@timeit
def get_market_details():
    global result
    with ThreadPoolExecutor(max_workers=60) as executor:
        executor.map(get_market_caps_per_page, (i for i in range(1, 11)))
        executor.shutdown(wait=True)
    # result = {i[0]:i[1] for i in  sorted(result.items(), key=lambda x: x[1].get('market_cap_rank'), reverse=False)}
    return result


if __name__ == '__main__':
    get_market_details()
