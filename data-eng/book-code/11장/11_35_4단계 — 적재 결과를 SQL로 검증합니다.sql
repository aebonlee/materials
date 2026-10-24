SELECT COUNT(*) AS total FROM quotes;

SELECT author, COUNT(*) AS cnt
FROM quotes
GROUP BY author
ORDER BY cnt DESC
LIMIT 5;

-- 태그가 쉼표로 이어져 있는 것도 확인 (10장에서 배운 1NF 위반입니다)
SELECT author, tags FROM quotes LIMIT 3;
