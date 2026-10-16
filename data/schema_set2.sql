-- Схема набору 2: Магазин. PostgreSQL 18.
-- Файл створює таблиці й наповнює їх початковими даними. Виконуйте його в ПОРОЖНІЙ схемі.

CREATE TABLE category (
    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    section varchar(60)
);

CREATE TABLE product (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku   varchar(12) NOT NULL UNIQUE,
    title  varchar(200) NOT NULL,
    category_id    integer NOT NULL REFERENCES category (id),
    price  numeric(10,2) NOT NULL CHECK (price >= 0),
    stock    integer NOT NULL DEFAULT 0 CHECK (stock >= 0),
    status varchar(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),
    added_on  date NOT NULL DEFAULT current_date
);

CREATE TABLE customer (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name  varchar(150) NOT NULL,
    email  varchar(120) NOT NULL UNIQUE,
    registered_on date NOT NULL DEFAULT current_date,
    bonus integer NOT NULL DEFAULT 0
);

CREATE TABLE purchase (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES customer (id),
    product_id   integer NOT NULL REFERENCES product (id),
    quantity    integer NOT NULL DEFAULT 1 CHECK (quantity > 0),
    ordered_on   date NOT NULL,
    shipped_on date
);

CREATE TABLE product_archive (
    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id    integer NOT NULL,
    sku      varchar(12) NOT NULL,
    title     varchar(200) NOT NULL,
    price     numeric(10,2) NOT NULL,
    note        varchar(100) NOT NULL,
    archived_on date NOT NULL DEFAULT current_date
);

CREATE TABLE purchase_archive (
    id        integer PRIMARY KEY,
    customer_id integer NOT NULL,
    product_id   integer NOT NULL,
    quantity    integer NOT NULL,
    ordered_on   date NOT NULL,
    shipped_on date,
    moved_on  date NOT NULL DEFAULT current_date
);

CREATE TABLE price_list (
    sku    varchar(12) PRIMARY KEY,
    new_price numeric(10,2) NOT NULL
);

CREATE TABLE supplier_feed (
    sku   varchar(12) PRIMARY KEY,
    title  varchar(200) NOT NULL,
    category_id    integer NOT NULL,
    price  numeric(10,2) NOT NULL,
    stock    integer NOT NULL
);

CREATE TABLE catalog_sync (
    sku   varchar(12) PRIMARY KEY,
    title  varchar(200) NOT NULL,
    category_id    integer NOT NULL,
    price  numeric(10,2) NOT NULL,
    stock    integer NOT NULL
);

CREATE TABLE audit_log (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note      varchar(200) NOT NULL,
    logged_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE stg_product (
    sku   text,
    title  text,
    category_id    text,
    price  text,
    stock    text,
    added_on  text
);

-- Початкові дані

INSERT INTO category (name, section) VALUES
    ('Напої', 'Бакалія'),
    ('Молочні вироби', 'Холодильні'),
    ('Хлібобулочні', 'Випічка'),
    ('Побутова хімія', 'Непродовольчі');

INSERT INTO product (sku, title, category_id, price, stock, status, added_on) VALUES
    ('SKU-0001', 'Кава зернова 1 кг', 1, 540.00, 12, 'active', '2025-01-12'),
    ('SKU-0002', 'Чай чорний 100 пакетиків', 1, 98.50, 40, 'active', '2025-01-12'),
    ('SKU-0003', 'Сік яблучний 1 л', 1, 54.90, 0, 'active', '2025-02-03'),
    ('SKU-0004', 'Молоко 2.5% 900 мл', 2, 42.00, 25, 'active', '2025-02-03'),
    ('SKU-0005', 'Йогурт натуральний', 2, 28.50, 3, 'active', '2025-02-20'),
    ('SKU-0006', 'Сир кисломолочний', 2, 76.00, 0, 'active', '2025-03-08'),
    ('SKU-0007', 'Хліб пшеничний', 3, 31.00, 18, 'active', '2025-03-08'),
    ('SKU-0008', 'Багет французький', 3, 39.00, 2, 'active', '2025-04-01'),
    ('SKU-0009', 'Пончик з кремом', 3, 24.50, 0, 'archived', '2025-04-01'),
    ('SKU-0010', 'Порошок пральний 3 кг', 4, 289.00, 9, 'active', '2025-04-15'),
    ('SKU-0011', 'Засіб для посуду', 4, 67.40, 15, 'active', '2025-05-06'),
    ('SKU-0012', 'Губки кухонні 5 шт.', 4, 35.00, 0, 'archived', '2025-05-06');

INSERT INTO customer (full_name, email, registered_on, bonus) VALUES
    ('Оксана Мороз', 'oksana.m@example.com', '2025-01-05', 10),
    ('Богдан Савчук', 'bohdan.s@example.com', '2025-01-30', 0),
    ('Галина Петренко', 'halyna.p@example.com', '2025-02-18', 4),
    ('Левко Радченко', 'levko.r@example.com', '2025-03-11', 0),
    ('Катерина Іваненко', 'kateryna.i@example.com', '2025-04-04', 7),
    ('Максим Захарчук', 'maksym.z@example.com', '2025-04-29', 2),
    ('Ірина Остапчук', 'iryna.o@example.com', '2025-05-21', 0),
    ('Тимур Гнатюк', 'tymur.h@example.com', '2025-06-12', 5),
    ('Олеся Крюк', 'olesia.k@example.com', '2025-07-01', 6);

INSERT INTO purchase (customer_id, product_id, quantity, ordered_on, shipped_on) VALUES
    (1, 1, 2, '2025-02-01', '2025-02-03'),
    (1, 4, 3, '2025-02-15', '2025-02-16'),
    (2, 2, 1, '2025-03-02', '2025-03-04'),
    (2, 7, 2, '2025-03-20', '2025-03-21'),
    (3, 5, 4, '2025-04-02', '2025-04-03'),
    (3, 9, 1, '2025-04-10', '2025-04-12'),
    (4, 10, 1, '2025-04-25', '2025-04-27'),
    (4, 11, 2, '2025-05-06', NULL),
    (5, 3, 3, '2025-05-18', '2025-05-20'),
    (5, 12, 2, '2025-06-01', '2025-06-03'),
    (6, 8, 1, '2025-06-14', NULL),
    (6, 1, 1, '2025-06-28', '2025-06-30'),
    (7, 2, 5, '2025-07-03', '2025-07-05'),
    (7, 9, 2, '2025-07-19', NULL),
    (8, 6, 1, '2025-08-01', '2025-08-02'),
    (8, 10, 2, '2025-08-15', NULL);

INSERT INTO price_list (sku, new_price) VALUES
    ('SKU-0002', 105.00),
    ('SKU-0005', 29.90),
    ('SKU-0007', 33.50),
    ('SKU-0010', 279.00),
    ('SKU-9999', 10.00);

INSERT INTO supplier_feed (sku, title, category_id, price, stock) VALUES
    ('SKU-0001', 'Кава зернова 1 кг', 1, 520.00, 20),
    ('SKU-0003', 'Сік яблучний 1 л', 1, 59.00, 30),
    ('SKU-0006', 'Сир кисломолочний', 2, 72.00, 15),
    ('SKU-0008', 'Багет французький', 3, 39.00, 10),
    ('SKU-0101', 'Йогурт грецький', 2, 38.50, 40),
    ('SKU-0102', 'Кефір 1%', 2, 36.00, 25);

INSERT INTO catalog_sync (sku, title, category_id, price, stock) VALUES
    ('SKU-0001', 'Кава зернова 1 кг', 1, 540.00, 12),
    ('SKU-0002', 'Чай чорний 100 пакетиків', 1, 102.00, 40),
    ('SKU-0004', 'Молоко 2.5% 900 мл', 2, 42.00, 30),
    ('SKU-0005', 'Йогурт натуральний', 2, 28.50, 3),
    ('SKU-0007', 'Хліб пшеничний', 3, 33.00, 18),
    ('SKU-0008', 'Багет французький', 3, 39.00, 6),
    ('SKU-0010', 'Порошок пральний 3 кг', 4, 289.00, 9),
    ('SKU-0011', 'Засіб для посуду', 4, 70.00, 20),
    ('SKU-0201', 'Мед липовий 500 г', 3, 210.00, 7),
    ('SKU-0202', 'Печиво вівсяне', 3, 45.00, 22);

INSERT INTO audit_log (note) VALUES
    ('Початкове завантаження асортименту'),
    ('Перевірка цін'),
    ('Імпорт покупців'),
    ('Резервна копія');
