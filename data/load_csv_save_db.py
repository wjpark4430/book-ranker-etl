import pandas as pd
import re
from sqlalchemy import text
from db.db_connector import get_engine
from ast import literal_eval


def load_csv_save_mysql(parse_contributors, file_path):
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
                        "price": int(re.sub(r"[^\d]", "", str(row["price"]))),
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
                conn.execute(
                    book_rank_insert,
                    {
                        "book_id": book_id,
                        "book_rank": int(row["book_rank"]),
                        "date_added": row["date_added"],
                    },
                )

                # 3. 기여자 파싱 및 저장

                try:
                    author_data = literal_eval(row["author"])
                except (ValueError, SyntaxError):
                    author_data = row["author"]

                if isinstance(author_data, str):
                    parsed = parse_contributors(author_data)
                elif isinstance(author_data, list):
                    parsed = author_data  # 이미 파싱된 경우
                else:
                    parsed = []

                for contributor in parsed:
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
