import pickle
import os
import sys
import traceback
import time

import pandas as pd
import urllib.request
import requests
import yfinance as yf
from tqdm import tqdm

comp_name = pd.read_csv("NYSE.txt", sep="\t", header=None, names=["Symbol", "Description"])
comp_name.columns = ['Symbol', 'Description']
comp_name = comp_name['Symbol'].tolist()

print('Beginning file download with urllib2...')


# for i in comp_name:
#     url = "https://query1.finance.yahoo.com/v7/finance/download/{}?" \
#           "period1=1442880000&period2=1600732800&interval=1d&events=history`".format(i)
#     response = requests.get(url)
#     if response.status_code != 200:  # could also check == requests.codes.ok
#         continue
#     urllib.request.urlretrieve(url, "./historical_data/{}.csv".format(i))

# https://query1.finance.yahoo.com/v7/finance/download/PTON?period1=1442880000&period2=1600732800&interval=1d&events=history`

# Get sector info
def load_from_pickle(file_path, default=None):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
    else:
        data = default

    return data


print('Collect company sectors')

# load previous saved data
sector_info = load_from_pickle(file_path='historical_data/sector_data.pkl', default={})
error_tickers = []
comp_info_all = load_from_pickle(file_path='historical_data/comp_info_all.pkl', default=[])
comp_info_all_names = [list(d.keys())[0] for d in comp_info_all]

# collect new data
for name in tqdm(comp_name):
    if name in comp_info_all_names:
        continue

    comp = yf.Ticker(name)
    comp_info = ''
    try:
        comp_info = comp.info
        comp_sector = comp_info['sector']
    except Exception as e:
        print(f'Error while processing {name}:')
        print(''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])))
        error_tickers.append(name)
        continue

    if comp_sector in sector_info.keys():
        sector_info[comp_sector].append(name)
    else:
        sector_info[comp_sector] = [name]

    comp_info_all.append({name: comp_info})

# save results to pickle
with open('historical_data/sector_data.pkl', 'wb') as f:
    pickle.dump(sector_info, f)

with open('historical_data/error_data.pkl', 'wb') as f:
    pickle.dump(error_tickers, f)

with open('historical_data/comp_info_all.pkl', 'wb') as f:
    pickle.dump(comp_info_all, f)
