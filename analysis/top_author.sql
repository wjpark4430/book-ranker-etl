-- 누적 등장 횟수가 많은 저자 TOP 5
SELECT p.name as author,
    COUNT(*) AS freq
FROM book_rank r
    JOIN book b ON r.book_id = b.id
    JOIN contribute c ON b.id = c.book_id
    JOIN person p ON c.person_id = p.id
GROUP BY p.name
ORDER BY freq DESC
LIMIT 5;