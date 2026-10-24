# 나쁜 예 — 어느 것이 남을지 보장되지 않습니다
clean = raw.dropDuplicates(["order_id"])

# 좋은 예 — "가장 최근 order_date를 남긴다"는 규칙을 명시
from pyspark.sql import Window, functions as F

# order_date가 같은 행이 둘 이상이면 그 안에서는 다시 정해지지 않습니다 — 정렬 열을 하나 더 둡니다
#   실습 코드: .orderBy(F.col("order_date").desc(), F.col("src_file").desc())  ← src_file = 원천 파일 이름
w = Window.partitionBy("order_id").orderBy(F.col("order_date").desc())
clean = (raw.withColumn("rn", F.row_number().over(w))
            .filter("rn = 1")
            .drop("rn"))
