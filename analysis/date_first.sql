-- 날짜별 랭킹 1위 도서
SELECT date_added, title, author
FROM book_rank
WHERE rank = 1
ORDER BY date_added;
