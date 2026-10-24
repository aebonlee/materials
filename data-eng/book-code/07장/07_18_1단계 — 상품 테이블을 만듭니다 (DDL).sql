CREATE TABLE products (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  name     VARCHAR(100) NOT NULL,
  category VARCHAR(50)  NOT NULL,
  price    INT          NOT NULL,
  stock    INT          NOT NULL DEFAULT 0
);

SHOW TABLES;
DESC products;
