SELECT ym, category, amount,
       ROW_NUMBER() OVER (PARTITION BY ym ORDER BY amount DESC) AS rn,
       RANK()       OVER (PARTITION BY ym ORDER BY amount DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY ym ORDER BY amount DESC) AS dense
FROM monthly_sales
ORDER BY ym, amount DESC;
