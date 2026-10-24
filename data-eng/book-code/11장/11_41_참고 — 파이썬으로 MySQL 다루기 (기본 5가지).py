# mysql_python_basics.py — 파이썬으로 MySQL 다루기 기본 5가지 (7장의 de-mysql · shop DB)
import pymysql

# ① 연결 — 한글이 깨지지 않게 charset은 utf8mb4, 결과를 dict로 받으면 칸 이름으로 꺼낼 수 있다
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='dataeng123',
                       database='shop', charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

with conn.cursor() as cur:
    # ② 읽기 — 값은 문자열로 이어 붙이지 말고 %s 자리로 넘긴다(SQL 인젝션 방지)
    cur.execute("SELECT id, name, price FROM products WHERE price >= %s ORDER BY price DESC", (20000,))
    for row in cur.fetchall():
        print(row['id'], row['name'], row['price'])

    # ③ 여러 행 한 번에 넣기 — executemany
    cur.execute("CREATE TEMPORARY TABLE tmp_orders (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, qty INT)")
    cur.executemany("INSERT INTO tmp_orders (product_id, qty) VALUES (%s, %s)", [(1, 2), (3, 1), (5, 4)])
    conn.commit()                                  # ④ commit 해야 확정된다
    cur.execute("SELECT COUNT(*) AS n FROM tmp_orders"); print('주문', cur.fetchone()['n'], '건')

    # ⑤ 트랜잭션 — 중간에 실패하면 rollback으로 통째로 되돌린다
    try:
        cur.execute("INSERT INTO tmp_orders (product_id, qty) VALUES (%s, %s)", (2, 1))
        cur.execute("INSERT INTO no_such_table VALUES (1)")   # 일부러 실패
        conn.commit()
    except pymysql.MySQLError as e:
        conn.rollback()
        print('되돌림:', e.args[1])
    cur.execute("SELECT COUNT(*) AS n FROM tmp_orders"); print('되돌린 뒤', cur.fetchone()['n'], '건')

conn.close()
