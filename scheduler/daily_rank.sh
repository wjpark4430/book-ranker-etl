#!/bin/bash

# 1. 프로젝트 디렉터리로 이동
cd "$(dirname "$0")/.." || exit

# 2. 크롤링 실행
echo "[`date`] 크롤링 시작"
python -u crawler/yes24_crawler.py
python -u crawler/aladin_crawler.py

# 3. DB 저장 실행
echo "[`date`] DB 저장 시작"
python db/save_to_db_aladin.py
python db/save_to_db_yes24.py

echo "[`date`] 작업 완료"