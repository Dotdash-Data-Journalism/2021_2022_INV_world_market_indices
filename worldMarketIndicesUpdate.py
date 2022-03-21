import yfinance as yf
import time
import pandas as pd
import os
import requests
from datetime import datetime
import pytz

# Function used to add new data to datawrapper chart via a pandas dataframe and 
# places the latest update date in the chart notes
def updateChart(dw_chart_id, dataSet, updateTitle, updateDate, dw_api_key):

    headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {dw_api_key}"
    }

    stringDataSet = dataSet.to_csv(path_or_buf=None, index=False, header=True)   

    dataRefresh = requests.put(url=f"https://api.datawrapper.de/v3/charts/{dw_chart_id}/data", 
    data=stringDataSet,
    headers={"Authorization": f"Bearer {dw_api_key}"}
    )

    dataRefresh.raise_for_status()

    time.sleep(2)

    callBack = {"title": updateTitle,
                "metadata": {
                    "annotate": {
                        "notes": f"Data from Yahoo Finance. Updated {updateDate}"
                    }
                }
            }
    notesRes = requests.patch(url=f"https://api.datawrapper.de/v3/charts/{dw_chart_id}",
    json=callBack,
    headers=headers)

    notesRes.raise_for_status()

    time.sleep(2)

    publishRes = requests.post(url=f"https://api.datawrapper.de/v3/charts/{dw_chart_id}/publish",
    headers=headers)

    publishRes.raise_for_status()

    time.sleep(2)

    imgHeaders = {
        "Accept": "image/png",
        "Authorization": f"Bearer {dw_api_key}"
        }
    pngDwnldRes = requests.get(url=f"https://api.datawrapper.de/v3/charts/{dw_chart_id}/export/png?unit=px&mode=rgb&plain=false&scale=1&zoom=2&download=false&fullVector=false&ligatures=true&transparent=false&logo=auto&dark=false",
    headers=imgHeaders)

    pngDwnldRes.raise_for_status()



ACCESS_TOKEN = os.getenv('DW_API_KEY')

wm = yf.Tickers("^AORD ^BSESN ^N225 ^KS11 399001.SZ 000001.SS ^HSI ^FCHI ^GDAXI ^FTSE ^TA125.TA ^GSPTSE ^GSPC")

pctCngList = []

for key, value in wm.tickers.items():
    time.sleep(1)
    stock = value.info
    pctCng = str(round(((stock['regularMarketPrice'] - stock['previousClose']) / stock['previousClose']) * 100, 2)) + '%'
    pctCngList.append(pctCng)

vmDict = {'Index': ['Australian All :au:',
                    'S&P BSE SENSEX :in:',
                    'NIKKEI 225 :jp:',
                    'Korea KOSPI :kr:',
                    'Shenzhen Component :cn:',
                    'SSE Shanghai Composite :cn:',
                    'Hang Seng :hk:',
                    'CAC 40 :fr:',
                    'Deutsche Boerse DAX :de:',
                    'FTSE 100 :gb:',
                    'Tel Aviv 125 :il:',
                    'S&P/TSX Composite :ca:',
                    'S&P 500 :us:'
], 'Change %': pctCngList}

wmDF = pd.DataFrame(data=vmDict)

wmDF.to_csv("worldMarketIndices.csv", index=False)

time.sleep(2)

EST = pytz.timezone('US/Eastern')
rightnow = datetime.now(EST)
rightnowformated = rightnow.strftime('%H:%M %p %Z')
fileDate = str(datetime.today().strftime('%B %d, %Y'))
chartTitle = f"World Market Indices at {str(rightnowformated)}"


updateChart("AVLCt", wmDF, chartTitle, fileDate, ACCESS_TOKEN)

# wfCSV = wmDF.to_csv(index=False)

# url = 'https://api.datawrapper.de/v3/charts/AVLCt/data'

# headers = {
#     'authorization':f'{DW_API}',
#     'content-type': 'text/csv'
# }
# r = requests.put(url, data=wfCSV, headers=headers)

# r.raise_for_status()

# urltwo = 'https://api.datawrapper.de/v3/charts/AVLCt'

# headerstwo = {
#     'authorization':f'{DW_API}',
#     'content-type': 'application/json'
# }

# EST = pytz.timezone('US/Eastern')
# rightnow = datetime.now(EST)
# rightnowformated = rightnow.strftime('%H:%M %p')
# rtwo = requests.patch(urltwo, data={'title': f'World Market Indices at {rightnowformated}'}, headers=headerstwo)

# rtwo.raise_for_status()

# urlthree = "https://api.datawrapper.de/v3/charts/AVLCt/publish"

# headersthree = {'authorization':f'{DW_API}'}
# rthree = requests.post(urlthree, headers=headersthree)
# rthree.raise_for_status()