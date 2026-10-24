# 2단계 — roundtrip.py 끝에 이어 붙입니다. DataFrame을 SQL로
grade_summary = duckdb.sql("""
    SELECT grade2 AS grade, count(*) AS users, avg(spend) AS avg_spend
    FROM top
    GROUP BY grade2
    ORDER BY avg_spend DESC
""").df()
print(grade_summary)
