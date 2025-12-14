-- LR8 migration: view for order reports
-- Columns:
--   report_at      - day of report (DATE)
--   order_id       - order id
--   count_product  - total quantity of products in the order

DROP VIEW IF EXISTS order_report;

CREATE VIEW order_report AS
SELECT
    DATE(o.created_at) AS report_at,
    o.id AS order_id,
    COALESCE(SUM(oi.quantity), 0) AS count_product
FROM orders AS o
LEFT JOIN order_items AS oi ON oi.order_id = o.id
GROUP BY DATE(o.created_at), o.id;
