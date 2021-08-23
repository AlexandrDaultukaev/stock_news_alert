import os
import requests
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
news_URL = "https://newsapi.org/v2/top-headlines"
stock_URL = "https://www.alphavantage.co/query"

load_dotenv()
news_API = os.getenv("API_KEY")
stock_API = os.getenv("STOCK_API")

news_params = {
    "apiKey": news_API,
    "q": COMPANY_NAME,
}

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_API,
}


def find_percentage(stk):
    day = int(list(stk["Time Series (Daily)"].keys())[0].split("-")[2])
    month = list(stk["Time Series (Daily)"].keys())[0].split("-")[1]
    year = list(stk["Time Series (Daily)"].keys())[0].split("-")[0]
    print(stk)
    yesterday = day - 1
    if day < 10:
        day = f"0{day}"
    if yesterday < 10:
        yesterday = f"0{yesterday}"

    if float(stk["Time Series (Daily)"][f"{year}-{month}-{day}"]["4. close"]) > \
            float(stk["Time Series (Daily)"][f"{year}-{month}-{yesterday}"]["4. close"]):
        print("Stock price increase")
    else:
        print("Stock price decrease")



def find_description(art):
    for num_article in range(int(art["totalResults"])):
        if art["articles"][num_article]["description"] not in ["", " "]:
            return num_article


response = requests.get(news_URL, params=news_params)
response.raise_for_status()
articles = response.json()

response = requests.get(stock_URL, params=stock_params)
response.raise_for_status()
stock_news = response.json()
find_percentage(stock_news)

num_art = find_description(articles)
title = articles["articles"][num_art]["title"]
description = articles["articles"][num_art]["description"]

print(f"Headline: {title}\n\nBrief: {description}")
