# Investopedia World Market Indices

This repository calculates the daily percent change in price of these 13 global financial indices:
Australian All, S&P BSE SENSEX, NIKKEI 225, Korea KOSPI, Shenzhen Component, SSE Shanghai Composite, Hang Seng, CAC 40, Deutsche Boerse DAX, FTSE 100, Tel Aviv 125, S&P/TSX Composite, S&P 500.

Data is gathered every hour from `yfinance` the [Python wrapper](https://pypi.org/project/yfinance/) for the [Yahoo Finance API](https://blog.api.rakuten.net/api-tutorial-yahoo-finance/). Data is then compiled into the CSV file `worldmarketIndices.csv` and used for a [Datawrapper](https://app.datawrapper.de) visualization in the [Investopedia](https://investopedia.com) daily newsletter. The data in the CSV file is updated hourly between the hours of 6AM & 11AM EST.