# crawler/yes24_crawler.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
import pandas as pd
import time

def fetch_yes24_bestsellers():
    url = "https://www.yes24.com/Product/Category/BestSeller"
    headers = {
        "User-Agent": "Mozilla/5.0 "
    }
    driver = webdriver.Chrome() 
    driver.get(url)

    time.sleep(3) 
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    books = []
    today = datetime.today().strftime('%Y-%m-%d')

    items = soup.select("#yesBestList > li")

    for idx, item in enumerate(items, start=1):
        title = item.select_one(".gd_name").get_text(strip=True)
        author = item.select_one(".authPub.info_auth").get_text(strip=True)
        publisher = item.select_one(".authPub.info_pub").get_text(strip=True)
        price = item.select_one(".yes_b").get_text(strip=True)
        
        books.append({
            "rank": idx,
            "title": title,
            "author": author,
            "publisher": publisher,
            "price": price,
            "date": today
        })

    df = pd.DataFrame(books)
    df.to_csv(f"data/yes24_{today}.csv", index=False)
    print(f"{len(df)}개 도서 저장 완료")

if __name__ == "__main__":
    fetch_yes24_bestsellers()
