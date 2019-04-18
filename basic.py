from googlesearch import search, search_news
from bs4 import BeautifulSoup
import re
from datetime import date
import urllib.request
from time import sleep
from googleapiclient.discovery import build

query = "site:cnn.com U.S. China Trade War"
site = "cnn.com"
title_class = "pg-headline"
num_search_url = 100

CSE_ID = "001991282022784705633:tfydvzge3ue"
API_KEY = "AIzaSyCO0YDXwTFGkgjjEbEXj-wWOhzjFMUkmMA"


def extract_date(url):
    list_dates = re.findall(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', url)
    if list_dates:
        news_date = list_dates[0]
        return date(int(news_date[0]), int(news_date[1]), int(news_date[2]))
    else:
        return None

def extract_pagehead(url):
    sleep(0.1)
    urlf = urllib.request.urlopen(url)
    soup =  BeautifulSoup(urlf, "html.parser" )
    pagehead = soup.find_all("h1")[0]
    return pagehead.text
  

def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=search_term, cx=CSE_ID, **kwargs).execute()
    return res

list_url = list(search_news(query, tld="co.in", num=num_search_url, stop=num_search_url, pause=3))
current_date = date.today()

list_info = []

print("extracting timeline.....")
for url in list_url:
    news_date = extract_date(url)
    if news_date:
        if news_date < current_date:
            current_date = news_date
            pagehead = extract_pagehead(url)
            list_info.append([news_date, pagehead, url])
            print(news_date)
            print(pagehead)
            print(url)
            print(" ")


            

