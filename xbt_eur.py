import krakenex
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


api = krakenex.API()

ohlc = api.query_public('OHLC', {'pair': 'XBTEUR',
                                 'interval': '1440'})

trades = api.query_public('Trades', {'pair': 'XBTEUR'})

ohlc = ohlc['result']['XXBTZEUR']
trades = trades['result']['XXBTZEUR']

time, o, h, l, c, v = (np.zeros(len(ohlc)) for i in range(6))

for i in range(len(ohlc)):
    time[i] = ohlc[i][0]
    o[i] = ohlc[i][1]
    h[i] = ohlc[i][2]
    l[i] = ohlc[i][3]
    c[i] = ohlc[i][4]
    v[i] = ohlc[i][6]


df = pd.DataFrame(c, index=pd.to_datetime(time, unit='s'), columns=['price'])
df['SMA'] = df['price'].rolling(100).mean()
df['lower'] = df['SMA'] - 2*df['price'].rolling(100).std()
df['upper'] = df['SMA'] + 2*df['price'].rolling(100).std()
df['percent_b'] = (df['price']-df['lower']) / (df['upper']-df['lower'])
df['price_SMA'] = df['price'] / df['SMA']
df['daily_ret'] = df['price'] / df['price'].shift(1)
df['cum_ret'] = df['daily_ret'].cumprod()
df_r = df[['percent_b','price_SMA','daily_ret']]


df_r.plot(grid=True, figsize=(13,8))
plt.show()
