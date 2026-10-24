CREATE TABLE monthly_sales (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  category VARCHAR(50) NOT NULL,
  ym       CHAR(7)     NOT NULL,   -- 'YYYY-MM'
  amount   INT         NOT NULL,
  UNIQUE KEY uq_cat_ym (category, ym)
);

INSERT INTO monthly_sales (category, ym, amount) VALUES
  ('전자', '2026-01', 1200), ('전자', '2026-02', 1500), ('전자', '2026-03', 1100),
  ('잡화', '2026-01',  400), ('잡화', '2026-02',  700), ('잡화', '2026-03',  900),
  ('식품', '2026-01',  800), ('식품', '2026-02',  600), ('식품', '2026-03', 1000);

SELECT COUNT(*) FROM monthly_sales;
SELECT * FROM monthly_sales ORDER BY category, ym;
