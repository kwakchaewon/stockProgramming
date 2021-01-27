import pandas as pd
import json
import urllib.request as req
from pandas import json_normalize

def drawingChart(symbol):

    #일별시세도표 json
    url = 'https://stockplus.com/api/securities/USA-'+symbol+'/day_candles.json?limit=20&to=2020-12-24T00%3A00%3A00.000%2B00%3A00'
    data = req.urlopen(url).read()
    dataj = json.loads(data.decode('utf-8'))

    tab = json_normalize(dataj["dayCandles"])

    newTab=tab[['date', 'tradePrice']]
    print(newTab)

    newTab= newTab.plot()
    return dataj
