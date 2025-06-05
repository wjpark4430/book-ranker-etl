-- 누적 등장 횟수가 많은 저자 TOP 5
SELECT author, COUNT(*) AS freq
FROM book_rank
GROUP BY author
ORDER BY freq DESC
LIMIT 5;
