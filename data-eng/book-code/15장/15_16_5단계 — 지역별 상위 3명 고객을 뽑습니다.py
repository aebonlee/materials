# 5단계(일부러 실패) — sql_analysis.py 끝에 이어 붙입니다
# 윈도 함수 결과(rnk)를 WHERE로 거르면?
try:
    duckdb.sql("""
        SELECT o.customer_id,
               rank() OVER (ORDER BY o.price DESC) AS rnk
        FROM 'orders_step1.parquet' AS o
        WHERE rnk <= 3
    """).fetchall()
except Exception as e:
    print('예상대로 실패:', e)
