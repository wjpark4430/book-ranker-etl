#!/bin/bash

TODAY=$(date '+%Y-%m-%d')

BASE_LOG_DIR="logs"
YES24_LOG_DIR="$BASE_LOG_DIR/yes24"
ALADIN_LOG_DIR="$BASE_LOG_DIR/aladin"
ETL_LOG_DIR="$BASE_LOG_DIR/etl"

YES24_LOG="$YES24_LOG_DIR/$TODAY.log"
ALADIN_LOG="$ALADIN_LOG_DIR/$TODAY.log"
ETL_LOG="$ETL_LOG_DIR/$TODAY.log"

cd "$(dirname "$0")/.." || exit 1

for DIR in "$YES24_LOG_DIR" "$ALADIN_LOG_DIR" "$ETL_LOG_DIR"; do
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
  fi
done


echo "[`date`] ETL 자동화 시작" | tee -a "$ETL_LOG"

### ---------------- YES24 처리 흐름 ---------------- ###
echo "[`date`] [YES24] 크롤링 시작" | tee -a "$ETL_LOG"

PYTHONIOENCODING=utf-8 python -u -m crawler.yes24_crawler >> "$YES24_LOG" 2>&1

if [ $? -eq 0 ]; then
  echo "[`date`] [YES24] 크롤링 성공 → DB 저장 시작" | tee -a "$ETL_LOG"
  PYTHONIOENCODING=utf-8 python -u -m db.save_to_db_yes24 >> "$YES24_LOG" 2>&1

  if [ $? -eq 0 ]; then
    echo "[`date`] [YES24] DB 저장 성공" | tee -a "$ETL_LOG"
  else
    echo "[`date`] [YES24] DB 저장 실패" | tee -a "$ETL_LOG"
  fi

else
  echo "[`date`] [YES24] 크롤링 실패 → DB 저장 건너뜀" | tee -a "$ETL_LOG"
fi

### ---------------- Aladin 처리 흐름 ---------------- ###
echo "[`date`] [Aladin] 크롤링 시작" | tee -a "$ETL_LOG"

PYTHONIOENCODING=utf-8 python -u -m crawler.aladin_crawler >> "$ALADIN_LOG" 2>&1

if [ $? -eq 0 ]; then
  echo "[`date`] [Aladin] 크롤링 성공 → DB 저장 시작" | tee -a "$ETL_LOG"
  PYTHONIOENCODING=utf-8 python -u -m db.save_to_db_aladin >> "$ALADIN_LOG" 2>&1

  if [ $? -eq 0 ]; then
    echo "[`date`] [Aladin] DB 저장 성공" | tee -a "$ETL_LOG"
  else
    echo "[`date`] [Aladin] DB 저장 실패" | tee -a "$ETL_LOG"
  fi

else
  echo "[`date`] [Aladin] 크롤링 실패 → DB 저장 건너뜀" | tee -a "$ETL_LOG"
fi

echo "[`date`] ETL 자동화 완료" | tee -a "$ETL_LOG"
