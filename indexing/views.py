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


def Table(request):
    time_frame = request.get_full_path_info().strip('/')
    all_coin_pairs = get_all_coin_pairs()
    # all_coin_pairs = ('1INCH/USDT','BAT/USDT','BEL/USDT','KEEP/USDT','LRC/USDT','MASK/USDT','SAND/USDT','SFP/USDT','MANA/USDT')
    if time_frame == 'all_tf':
        short_time_frames = ('1m','5m', '15m', '1h')
        long_time_frames = ('4h', '1d', '1w', '1M')
        all_time_frames = short_time_frames+long_time_frames
    else:
        all_time_frames = (time_frame,)
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
