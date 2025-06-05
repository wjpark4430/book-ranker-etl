import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

def load_csv_to_mysql():
    today = datetime.today().strftime('%Y-%m-%d')
    file_path = f"data/yes24_{today}.csv"

    try:
        df = pd.read_csv(file_path)
        print(f"CSV 파일 로드 완료: {file_path}")
    except FileNotFoundError:
        print("CSV 파일이 존재하지 않습니다.")
        return

    user = 'root'
    password = '1234'
    host = 'localhost'
    dbname = 'book_crawling'

    # SQLAlchemy 엔진 생성 (pymysql 사용)
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{dbname}")

    try:
        df['price'] = df['price'].str.replace(',', '').astype(int)
        df.to_sql(name='book_rank', con=engine, if_exists='append', index=False)
        print(f"{len(df)}건 데이터 MySQL에 삽입 완료")
    except Exception as e:
        print("DB 삽입 중 에러 발생:", e)

if __name__ == "__main__":
    load_csv_to_mysql()
