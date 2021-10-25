from datetime import datetime

from django.shortcuts import HttpResponse, render
from django.utils.timezone import make_aware

# Create your views here.
from indexing.management.commands.coingecko import get_market_details
from indexing.management.commands.elastic_index import main
from indexing.utils import get_all_coin_pairs
from .models import Market_Details


def home(request):
    return render(request, 'home.html')


def Table_1m(request):
    all_coin_pairs = get_all_coin_pairs()
    all_time_frames = ('1m',)
    df = main(all_coin_pairs, all_time_frames)
    required_coins = df.sort_values('atr_weightage', ascending=False)
    coin_object = required_coins.to_html()

    return HttpResponse(coin_object)


def Table_5m(request):
    all_coin_pairs = get_all_coin_pairs()
    all_time_frames = ('5m',)
    df = main(all_coin_pairs, all_time_frames)
    required_coins = df.sort_values('atr_weightage', ascending=False)
    coin_object = required_coins.to_html()

    return HttpResponse(coin_object)


def Table_1h(request):
    all_coin_pairs = get_all_coin_pairs()
    all_time_frames = ('1h',)
    df = main(all_coin_pairs, all_time_frames)
    required_coins = df.sort_values('atr_weightage', ascending=False)
    coin_object = required_coins.to_html()

    return HttpResponse(coin_object)


def market_details_refresh(request):
    market_details = get_market_details()
    for i in market_details.values():
        i['ath_date'] = make_aware(datetime.strptime(i['ath_date'][:19], '%Y-%m-%dT%H:%M:%S'))
        i['atl_date'] = make_aware(datetime.strptime(i['atl_date'][:19], '%Y-%m-%dT%H:%M:%S'))
        i['last_updated'] = make_aware(datetime.strptime(i['last_updated'][:19], '%Y-%m-%dT%H:%M:%S'))
        i['roi'] = 0.0
        m = Market_Details(**i)
        m.save()
    return HttpResponse("Market data Updated")
