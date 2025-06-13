#!/bin/bash
TODAY=$(date '+%Y-%m-%d')
LOG_FILE="logs/etl_$TODAY.log"

# 1. 프로젝트 디렉터리로 이동
cd "$(dirname "$0")/.." || exit

# 2. 크롤링 실행
echo "[`date`] 크롤링 시작"
PYTHONIOENCODING=utf-8 python -u -m crawler.yes24_crawler >> logs/yes24_etl_$TODAY.log 2>&1
PYTHONIOENCODING=utf-8 python -u -m crawler.aladin_crawler >> logs/aladin_etl_$TODAY.log 2>&1

# 3. DB 저장 실행
echo "[`date`] DB 저장 시작"
PYTHONIOENCODING=utf-8 python -u -m db.save_to_db_aladin >> logs/yes24_etl_$TODAY.log 2>&1
PYTHONIOENCODING=utf-8 python -u -m db.save_to_db_yes24 >> logs/aladin_etl_$TODAY.log 2>&1