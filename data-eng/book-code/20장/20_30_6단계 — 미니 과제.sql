-- 정답 예시 — 채널별 비중
SELECT channel,
       sum(amount) AS revenue,
       round(sum(amount) * 100.0 / sum(sum(amount)) OVER (), 1) AS pct
FROM iceberg.lakehouse.orders
GROUP BY channel
ORDER BY revenue DESC;
