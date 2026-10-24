# 3단계 — roundtrip.py 끝에 이어 붙입니다
# ① SQL — 100만 행에서 사용자별 요약으로 줄인다
users = duckdb.sql("""
    SELECT user_id,
           count(*) FILTER (WHERE event_type = 'view') AS views,
           count(*) FILTER (WHERE event_type = 'cart') AS carts,
           count(*) FILTER (WHERE event_type = 'buy')  AS buys,
           sum(value) FILTER (WHERE event_type = 'buy') AS spend
    FROM 'events.parquet'
    GROUP BY user_id
""").df()
print('① SQL 집계 후:', users.shape)

# ② Pandas — 전환율 계산과 라벨링 (세밀한 규칙)
users['cvr'] = (users['buys'] / users['views']).fillna(0).round(3)
users['segment'] = 'normal'
users.loc[users['cvr'] >= 0.1, 'segment'] = 'high_intent'
users.loc[users['buys'] == 0, 'segment'] = 'browser'
print('② Pandas 가공 후:', users.shape)

# ③ SQL — 세그먼트별 요약
seg = duckdb.sql("""
    SELECT segment,
           count(*) AS users,
           round(avg(cvr), 3) AS avg_cvr,
           round(avg(coalesce(spend, 0))) AS avg_spend
    FROM users
    GROUP BY segment
    ORDER BY users DESC
""").df()
print('③ 세그먼트 요약')
print(seg)
