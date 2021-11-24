import pandas as pd
import requests
import openpyxl
# import xlwings
# wb = xlwings.Book('waz_data.xlsx').sheets('Sheet1-Waz')
r=requests.get('https://api.wazirx.com/api/v2/market-status')
data_dict = dict(r.json())['markets']

df = pd.DataFrame()
d = []
d1={}
usdt_price=65
for i in data_dict:
    if i['type']=='SPOT' and i['quoteMarket'] in ('inr','usdt'):
        if i.get('baseMarket') == 'usdt':
            usdt_price = float(i['sell'])
        if not d1.get(i['baseMarket']):
            d1[i['baseMarket']] = {i['quoteMarket']+'sell':float(i['sell']),i['quoteMarket']+'buy':float(i['buy'])}
        else:
            d1[i['baseMarket']][i['quoteMarket']+'sell']=float(i['sell'])
            d1[i['baseMarket']][i['quoteMarket']+'buy']=float(i['buy'])

coins_list = []
for i in d1:
    temp = {'coin':i}
    temp.update(d1[i])
    coins_list.append(temp)
df =pd.DataFrame(coins_list)
df['usdt_price'] = usdt_price
# df['converted_buy'] =
df['inr-usdt-buy'] = df['inrbuy']/usdt_price
df['inr-usdt-sell'] = df['inrsell']/usdt_price
df['usdt-inr-buy'] = df['usdtbuy']*usdt_price
df['usdt-inr-sell'] = df['usdtsell']*usdt_price
df['buy-usdt-sell-inr'] = df['inr-usdt-sell']-df['usdtbuy']
df['buy-inr-sell-usdt'] = df['usdt-inr-sell'] - df['inrbuy']
df['bisu'] = (df['usdt-inr-buy']-df['inrsell'])*100/df['inrsell']
print('****done****')
print(usdt_price)
df.to_excel(r"/Users/rakeshreddy/Documents/Trading/wazirx-connector-python-master/output.xlsx")