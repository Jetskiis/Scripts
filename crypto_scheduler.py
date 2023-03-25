
import bs4
import requests
import time
import pandas as pd


try:
    res = requests.get('https://www.coinmarketcap.com/')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    print(soup.prettify())
except Exception as e:
    print(e)
