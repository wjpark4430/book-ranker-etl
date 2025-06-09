import pandas as pd
from datetime import datetime
from sqlalchemy import text
from db.db_connector import get_engine
import re


def parse_contributors(raw_text):
    contributors = []

    for part in raw_text.split("/"):
        match = re.match(r"(.+?)(저|역|글그림|그림|글|감수)$", part.strip())
        if match:
            name = match.group(1).strip()
            role = match.group(2)
            contributors.append({"name": name, "role": role})
        else:
            contributors.append({"name": part.strip(), "role": "기타"})
    return contributors


def load_csv_to_mysql():
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"data/yes24_{today}.csv"

    try:
        df = pd.read_csv(file_path)
        print(f"CSV 파일 로드 완료: {file_path}")
    except FileNotFoundError:
        print("CSV 파일이 존재하지 않습니다.")
        return

    try:
        engine = get_engine()
        conn = engine.connect()
        with engine.begin() as conn:
            for _, row in df.iterrows():
                # 1. book 저장 또는 중복 방지
                book_insert = text(
                    """
                    INSERT INTO book (title, publisher, price)
                    VALUES (:title, :publisher, :price)
                    ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
                    """
                )

                result = conn.execute(
                    book_insert,
                    {
                        "title": row["title"],
                        "publisher": row["publisher"],
                        "price": int(row["price"].replace(",", "")),
                    },
                )
                book_id = result.lastrowid

                # 2. book_rank 저장
                book_rank_insert = text(
                    """
                    INSERT INTO book_rank (book_id, book_rank, date_added)
                    VALUES (:book_id, :book_rank, :date_added)
                    """
                )
                result = conn.execute(
                    book_rank_insert,
                    {
                        "book_id": book_id,
                        "book_rank": int(row["book_rank"]),
                        "date_added": row["date_added"],
                    },
                )

                # 3. 기여자 파싱 및 저장
                contributors = parse_contributors(row["author"])

                for contributor in contributors:
                    # person 저장 또는 중복 방지
                    person_insert = text(
                        """
                        INSERT INTO person (name)
                        VALUES (:name)
                        ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
                        """
                    )
                    person_result = conn.execute(
                        person_insert, {"name": contributor["name"]}
                    )
                    person_id = person_result.lastrowid

                    # contribute 저장
                    contribute_insert = text(
                        """
                        INSERT INTO contribute (person_id, book_id, book_role)
                        VALUES (:person_id, :book_id, :book_role)
                        """
                    )
                    conn.execute(
                        contribute_insert,
                        {
                            "person_id": person_id,
                            "book_id": book_id,
                            "book_role": contributor["role"],
                        },
                    )

        print(f"{len(df)}건 데이터 MySQL에 삽입 완료")
        conn.close()

    except Exception as e:
        print("DB 삽입 중 에러 발생:", e)


if __name__ == "__main__":
    load_csv_to_mysql()
