-- 날짜별 랭킹 1위 도서 (YES24 데이터 기반)
WITH ranked_authors AS (
    SELECT r.date_added,
        b.title,
        p.name AS author,
        c.book_role,
        ROW_NUMBER() OVER (
            PARTITION BY r.id
            ORDER BY CASE
                    c.book_role
                    WHEN '저' THEN 1
                    WHEN '글' THEN 2
                    WHEN '글그림' THEN 3
                    WHEN '그림' THEN 4
                    WHEN '역' THEN 5
                    WHEN '감수' THEN 6
                    ELSE 9
                END
        ) AS rn
    FROM book_rank r
        JOIN book b ON r.book_id = b.id
        JOIN contribute c ON b.id = c.book_id
        JOIN person p ON c.person_id = p.id
    WHERE r.book_rank = 1
)
SELECT date_added,
    title,
    author,
    book_role
FROM ranked_authors
WHERE rn = 1
ORDER BY date_added;