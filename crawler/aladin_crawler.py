import os
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import setup_logger
from utils.retry import with_retry


def fetch_aladin_bestsellers():
    log = setup_logger("aladin_crawler")
    log.info("알라딘 베스트셀러 크롤링 시작")

    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1"

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

        items = soup.select(".ss_book_box")

        for idx, item in enumerate(items, start=1):
            if idx > 20:
                break

            try:
                title = item.select_one(".bo3").get_text(strip=True)
            except AttributeError:
                continue

            contributors = []

            author_li = item.select(".ss_book_list li")[2]

            if author_li:
                author_tags = author_li.find_all(
                    "a", href=lambda x: x and "AuthorSearch" in x
                )
                rest_text = author_li.get_text(" ", strip=True)

                role_match = re.search(r"\((.*?)\)", rest_text)
                common_role = (
                    role_match.group(1).strip() if role_match else "역할 정보 없음"
                )

                for author in author_tags:
                    name = author.text.strip()
                    contributors.append(f"{name}({common_role})")
            else:
                contributors.append("저자 정보 없음")

            publisher_link = item.find("a", href=lambda x: x and "PublisherSearch" in x)
            publisher = (
                publisher_link.get_text(strip=True)
                if publisher_link
                else "출판사 정보 없음"
            )

            price = item.select_one(".ss_p2").get_text(strip=True)

            log.info(
                f"Processing book {idx}: {title} by {contributors} ({publisher}) - {price}"
            )

            if title:
                books.append(
                    {
                        "book_rank": idx,
                        "title": title,
                        "author": contributors,
                        "publisher": publisher,
                        "price": price,
                        "date_added": today,
                    }
                )

            df = pd.DataFrame(books)

            if df.empty:
                log.error("[ALADIN-크롤링 오류] 도서 정보를 가져오지 못했습니다.")
                return

        output_dir = "data"
        output_file = f"{output_dir}/aladin_{today}.csv"

        try:
            os.makedirs(output_dir, exist_ok=True)
            df.to_csv(output_file, index=False)

            log.info(f"알라딘 에서 {len(df)}권 도서 저장 완료")
        except PermissionError:
            log.error("[ALADIN-CSV 저장 오류] 권한이 없어 파일을 저장할 수 없습니다.")
            raise
        except OSError as e:
            log.error(f"[ALADIN-CSV 저장 오류] 기타 저장 실패: {e}")
            raise
    except Exception as e:
        log.warning(f"[ALADIN-크롤링 오류] {e}")
        raise

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":

    log = setup_logger("aladin_crawler")

    with_retry(
        fetch_aladin_bestsellers,
        log,
        max_retries=3,
        delay=5,
        task_name="ALADIN 크롤링",
    )
