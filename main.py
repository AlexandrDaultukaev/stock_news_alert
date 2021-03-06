import os
import requests
import smtplib
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
news_URL = "https://newsapi.org/v2/top-headlines"
stock_URL = "https://www.alphavantage.co/query"

load_dotenv()
news_API = os.getenv("API_KEY")
stock_API = os.getenv("STOCK_API")
from_email = os.getenv("FROM_EMAIL")
mail = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

news_params = {
    "apiKey": news_API,
    "q": COMPANY_NAME,
}

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_API,
}


def send_to_email(ttle, desc, price):
    with smtplib.SMTP("smtp.gmail.com") as connecting:
        connecting.starttls()
        connecting.login(user=from_email, password=password)
        connecting.sendmail(from_addr=from_email, to_addrs=mail, msg=f"Subject: {price}\n\nHeadline: {ttle}\nBrief:"
                                                                     f" {desc}".encode("utf-8"))


def calc_percentage(today_p, yesterday_p):
    return round(abs(((today_p - yesterday_p) * 100) / yesterday_p), 3)


def find_percentage(stk):
    day = int(list(stk["Time Series (Daily)"].keys())[0].split("-")[2])
    month = list(stk["Time Series (Daily)"].keys())[0].split("-")[1]
    year = list(stk["Time Series (Daily)"].keys())[0].split("-")[0]
    yesterday = day - 1
    if day < 10:
        day = f"0{day}"
    if yesterday < 10:
        yesterday = f"0{yesterday}"
    today_price = float(stk["Time Series (Daily)"][f"{year}-{month}-{day}"]["4. close"])
    yesterday_price = float(stk["Time Series (Daily)"][f"{year}-{month}-{yesterday}"]["4. close"])
    if today_price > yesterday_price:
        percentage = calc_percentage(today_price, yesterday_price)
        return f"Stock price increase. ^ {percentage}%"
    else:
        percentage = calc_percentage(today_price, yesterday_price)
        return f"Stock price decrease. ∨ {percentage}%"


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
print(articles)
num_art = find_description(articles)

title = articles["articles"][num_art]["title"]
description = articles["articles"][num_art]["description"]
about_price = find_percentage(stock_news)

send_to_email(title, description, about_price)

