CREATE TABLE customers (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  tel  VARCHAR(20) NOT NULL
);

CREATE TABLE orders (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  ordered_at  DATETIME NOT NULL,
  CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE order_items (
  order_id   INT NOT NULL,
  product_id INT NOT NULL,
  quantity   INT NOT NULL,
  unit_price INT NOT NULL,   -- 주문 당시 확정 단가 (products.price와 다른 사실)
  PRIMARY KEY (order_id, product_id),
  CONSTRAINT fk_items_order   FOREIGN KEY (order_id)   REFERENCES orders (id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products (id)
);

SHOW TABLES;
