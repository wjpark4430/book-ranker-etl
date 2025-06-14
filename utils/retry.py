import time


def with_retry(task_func, logger, max_retries=3, delay=5, task_name="작업"):
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"[시도 {attempt}] {task_name} 시작")
            task_func()
            logger.info(f"{task_name} 성공")
            break
        except Exception as e:
            logger.error(f"[실패 {attempt}] {e}")
            if attempt < max_retries:
                logger.info(f"{delay}초 후 재시도합니다...")
                time.sleep(delay)
            else:
                logger.critical(f"{task_name} 최종 실패. 중단합니다.")
