import os
import requests
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

load_dotenv()
API = os.getenv("API_KEY")

params = {
    "apiKey": API,
    "q": COMPANY_NAME,
}


def find_description(art):
    for num_article in range(int(art["totalResults"])):
        if art["articles"][num_article]["description"] not in ["", " "]:
            return num_article


response = requests.get("https://newsapi.org/v2/top-headlines", params=params)
response.raise_for_status()

articles = response.json()
num_art = find_description(articles)
title = articles["articles"][num_art]["title"]
description = articles["articles"][num_art]["description"]

print(f"Headline: {title}\n\nBrief: {description}")
