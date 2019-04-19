from googlesearch import search, search_news
from bs4 import BeautifulSoup
import re
from keywords import simple_rake
from datetime import date
import urllib.request
from time import sleep
from googleapiclient.discovery import build
import embedding


site = "cnn.com"
title_class = "pg-headline"
num_search_url = 20

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


def recursive_search(query_input, date=date.today()):
    model = embedding.EmbeddingModel()
    query = "site:{} {}".format(site, query_input)
    list_url = list(search_news(query, tld="co.in", num=num_search_url, stop=num_search_url, pause=3))
    for url in list_url:
        news_date = extract_date(url)
        if news_date:
            if news_date < date:
                pagehead = extract_pagehead(url)
                keywords = simple_rake(pagehead)
                print(pagehead)
                for keyword in keywords:
                    print("{} : {}".format(keyword[0], model.phraseSimilarity(keyword[1], query_input)))


def google_search(query_input):
    query = "site:{} {}".format(site, query_input)
    list_url = list(search_news(query, tld="co.in", num=num_search_url, stop=num_search_url, pause=3))
    current_date = date.today()

    info = {'results':[]}

    print("extracting timeline.....")
    for url in list_url:
        news_date = extract_date(url)
        if news_date:
            if news_date < current_date:
                current_date = news_date
                pagehead = extract_pagehead(url)
                info['results'].append({
                    'date': news_date, 
                    'title' : pagehead, 
                    'url' : url})
                print(news_date)
                print(pagehead)
                print(url)
                print(simple_rake(pagehead))
                print(" ")
    return info

def main():
    recursive_search("China U.S. Trade War")

if __name__ == "__main__":
    main()

                

