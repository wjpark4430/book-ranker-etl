import os
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import setup_logger


def fetch_yes24_bestsellers():
    log = setup_logger("yes24_crawler")
    log.info("YES24 베스트셀러 크롤링 시작")

    url = "https://www.yes24.com/Product/Category/BestSeller"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        books = []
        today = datetime.today().strftime("%Y-%m-%d")

        items = soup.select("#yesBestList > li")

        for idx, item in enumerate(items, start=1):
            if idx > 20:
                break

            try:
                title = item.select_one(".gd_name").get_text(strip=True)
            except AttributeError:
                continue

            author = item.select_one(".authPub.info_auth").get_text(strip=True)
            publisher = item.select_one(".authPub.info_pub").get_text(strip=True)
            price = item.select_one(".yes_b").get_text(strip=True)

            log.info(
                f"Processing book {idx}: {title} by {author} ({publisher}) - {price}"
            )

            books.append(
                {
                    "book_rank": idx,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "price": price,
                    "date_added": today,
                }
            )

        df = pd.DataFrame(books)

        if df.empty:
            log.error("[YES24-크롤링 오류] 도서 정보를 가져오지 못했습니다.")
            return

        output_dir = "data"
        output_file = f"{output_dir}/yes24_{today}.csv"

        try:
            os.makedirs(output_dir, exist_ok=True)
            df.to_csv(output_file, index=False)

            log.info(f"YES24 에서 {len(df)}권 도서 저장 완료")
        except PermissionError:
            log.error("[YES24-CSV 저장 오류] 권한이 없어 파일을 저장할 수 없습니다.")
        except OSError as e:
            log.error(f"[YES24-CSV 저장 오류] 기타 저장 실패: {e}")

    except Exception as e:
        log.warning(f"[YES24-크롤링 오류] {e}")

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    fetch_yes24_bestsellers()
