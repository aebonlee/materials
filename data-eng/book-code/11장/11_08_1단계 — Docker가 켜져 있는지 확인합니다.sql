SHOW TABLES;          -- Empty set이 정상

CREATE TABLE quotes (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  author     VARCHAR(100) NOT NULL,
  quote_text TEXT NOT NULL,
  tags       VARCHAR(300),
  crawled_at DATETIME NOT NULL,
  UNIQUE KEY uq_author_text (author, quote_text(200))
);
DESC quotes;          -- 다섯 칸이 보이면 exit
