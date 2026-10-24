CREATE TABLE quotes (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  author     VARCHAR(100) NOT NULL,
  quote_text TEXT NOT NULL,          -- VARCHAR(500)이면 긴 명언이 잘립니다 (아래 설명)
  tags       VARCHAR(300),
  crawled_at DATETIME NOT NULL,
  UNIQUE KEY uq_author_text (author, quote_text(200))
);

DESC quotes;
