import numpy as np
import pandas as pd
import requests
from tabulate import tabulate

req = requests.get("https://api.llama.fi/protocols")

from defillama import DefiLlama

# initialize api client
llama = DefiLlama()

# Get all protocols data
response = llama.get_all_protocols()

dexs = []
for i in response:
    if i['category'] == 'Dexes':
        dexs.append(i)

d = {}
for i in dexs:
    d[i["name"]] = []
    count = 0
    for j in i['chainTvls']:
        count += i['chainTvls'][j]
    res=[]
    res.append(count)
    res.append(i['change_1h'])
    res.append(i['change_1d'])
    res.append(i['change_7d'])
    d[i["name"]] = res

df = pd.DataFrame(d).T
df.columns = ['Total Value Locked', '1 Hour change', '1 Day Change', '7 Day Change']
df = df.sort_values(by='Total Value Locked', ascending=False)
df.index.name = 'Protocol Name'

print(tabulate(df.head(100), headers='keys', tablefmt='psql'))