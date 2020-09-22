
import pandas as pd
import urllib.request
import requests

comp_name = pd.read_csv("NYSE.txt", sep=" ", header=None,names=["Symbol", "Description"])
comp_name.columns = ['Symbol','Description']
comp_name = comp_name['Symbol'].tolist()

print('Beginning file download with urllib2...')



for i in comp_name:
    j = (i.split("\t")[0])
    url = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1442880000&period2=1600732800&interval=1d&events=history`".format(j)
    response = requests.get(url)
    if response.status_code != 200: #could also check == requests.codes.ok
        continue
    urllib.request.urlretrieve(url, "./historical_data/{}.csv".format(j))

#https://query1.finance.yahoo.com/v7/finance/download/PTON?period1=1442880000&period2=1600732800&interval=1d&events=history`