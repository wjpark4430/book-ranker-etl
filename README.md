## 📚 도서 베스트셀러 수집 및 분석 시스템

국내 주요 서점의 베스트셀러 정보를 주기적으로 수집하고, 이를 MySQL에 저장하여 향후 분석할 수 있도록 구성된 데이터 수집 자동화 프로젝트입니다.

---

### 📌 프로젝트 개요

* **목표**: 베스트셀러 도서 정보를 수집, 정제, 저장하여 분석 가능한 형태로 구성
* **주요 대상**: YES24 베스트셀러
* **구현 언어**: Python
* **DB**: MySQL
* **배포 방식**: 로컬 또는 추후 서버 자동화 스크립트

---

### 🛠 기술 스택

| 구분     | 기술                        |
| ------ | ------------------------- |
| 크롤링    | Selenium, BeautifulSoup   |
| 데이터 처리 | pandas                    |
| DB 연동  | pymysql, sqlalchemy       |
| 실행 환경  | Python 3.11.7 (Anaconda 기반) |

---

### 📁 프로젝트 구조

```
book-ranker-etl/
│
├── crawler/                # 웹 크롤링 모듈
│   └── yes24_crawler.py
│
├── db/               # DB 연결 및 쿼리 관련 코드
│   ├── create_tables.sql          # 테이블 생성 SQL
│   └── save_to_db.py
│
├── data/                   # 수집된 CSV 데이터 저장 폴더
│
├── analysis/               # 분석용 SQL 또는 시각화
│   
├── scheduler/              # 자동화 스크립트 (로컬 실행용 .sh 등)
│   ├── daily_rank_win.bat
│   └── daily_rank.sh
│
├── requirements.txt        # 필요 패키지 목록
└── README.md               # 프로젝트 설명 파일
```

---

### ✅ 기능 설명

* YES24 베스트셀러 도서 정보 크롤링 (제목, 저자, 출판사, 가격 등)
* 수집된 데이터를 `.csv`로 저장
* 중복 방지를 위한 DB 삽입 로직 포함
* 날짜별 랭킹 데이터 축적 가능

---

### 🔄 실행 방법

1. **환경 구성**

   ```bash
   pip install -r requirements.txt
   ```

2. **MySQL DB 테이블 생성**

   ```sql
    -- create_tables.sql 참고
    CREATE TABLE IF NOT EXISTS book_rank (
        id INT PRIMARY KEY,
        book_rank INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        publisher VARCHAR(255) NOT NULL,
        price INT NOT NULL,
        date_added DATE NOT NULL,
        UNIQUE KEY unique_book (title, date_added)
    );
   ```

3. **크롤러 실행**

   ```bash
   python crawler/yes24_crawler.py
   ```

4. **자동화 스크립트 실행**

   ```bash
   ./scheduler/run_daily.sh
   ```

---

### ⚠️ 예외 처리

* 브라우저 창 오류 또는 셀레니움 비정상 종료 대비 `try-except` 문 적용
* 중복 도서 정보는 DB에서 무시되도록 설정 (UNIQUE 제약)

---

### ✍️ 추후 계획

* 교보문고, 알라딘 등 타 서점 추가
* 일자별 랭킹 변화 시각화
* Streamlit 등을 활용한 간단한 웹 대시보드 구현