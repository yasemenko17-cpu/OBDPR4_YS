"""Схеми й початкові дані трьох наборів (збігаються з файлами data/schema_setN.sql)."""

SCHEMAS = {1: '-- Схема набору 1: Бібліотека. PostgreSQL 18.\n'
    '-- Файл створює таблиці й наповнює їх початковими даними. Виконуйте його в ПОРОЖНІЙ схемі.\n'
    '\n'
    'CREATE TABLE publisher (\n'
    '    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    name varchar(100) NOT NULL UNIQUE,\n'
    '    city varchar(60)\n'
    ');\n'
    '\n'
    'CREATE TABLE book (\n'
    '    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    isbn   char(13) NOT NULL UNIQUE,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    publisher_id    integer NOT NULL REFERENCES publisher (id),\n'
    '    price  numeric(10,2) NOT NULL CHECK (price >= 0),\n'
    '    copies    integer NOT NULL DEFAULT 0 CHECK (copies >= 0),\n'
    "    status varchar(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),\n"
    '    added_on  date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE reader (\n'
    '    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    full_name  varchar(150) NOT NULL,\n'
    '    email  varchar(120) NOT NULL UNIQUE,\n'
    '    registered_on date NOT NULL DEFAULT current_date,\n'
    '    bonus integer NOT NULL DEFAULT 0\n'
    ');\n'
    '\n'
    'CREATE TABLE loan (\n'
    '    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    reader_id integer NOT NULL REFERENCES reader (id),\n'
    '    book_id   integer NOT NULL REFERENCES book (id),\n'
    '    copies    integer NOT NULL DEFAULT 1 CHECK (copies > 0),\n'
    '    loaned_on   date NOT NULL,\n'
    '    returned_on date\n'
    ');\n'
    '\n'
    'CREATE TABLE book_archive (\n'
    '    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    book_id    integer NOT NULL,\n'
    '    isbn      char(13) NOT NULL,\n'
    '    title     varchar(200) NOT NULL,\n'
    '    price     numeric(10,2) NOT NULL,\n'
    '    note        varchar(100) NOT NULL,\n'
    '    archived_on date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE loan_archive (\n'
    '    id        integer PRIMARY KEY,\n'
    '    reader_id integer NOT NULL,\n'
    '    book_id   integer NOT NULL,\n'
    '    copies    integer NOT NULL,\n'
    '    loaned_on   date NOT NULL,\n'
    '    returned_on date,\n'
    '    moved_on  date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE price_list (\n'
    '    isbn    char(13) PRIMARY KEY,\n'
    '    new_price numeric(10,2) NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE supplier_feed (\n'
    '    isbn   char(13) PRIMARY KEY,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    publisher_id    integer NOT NULL,\n'
    '    price  numeric(10,2) NOT NULL,\n'
    '    copies    integer NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE catalog_sync (\n'
    '    isbn   char(13) PRIMARY KEY,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    publisher_id    integer NOT NULL,\n'
    '    price  numeric(10,2) NOT NULL,\n'
    '    copies    integer NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE audit_log (\n'
    '    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    note      varchar(200) NOT NULL,\n'
    '    logged_at timestamptz NOT NULL DEFAULT now()\n'
    ');\n'
    '\n'
    'CREATE TABLE stg_book (\n'
    '    isbn   text,\n'
    '    title  text,\n'
    '    publisher_id    text,\n'
    '    price  text,\n'
    '    copies    text,\n'
    '    added_on  text\n'
    ');\n'
    '\n'
    '-- Початкові дані\n'
    '\n'
    'INSERT INTO publisher (name, city) VALUES\n'
    "    ('Фабула', 'Харків'),\n"
    "    ('Старий Лев', 'Львів'),\n"
    "    ('Ранок', 'Харків'),\n"
    "    ('Основи', 'Київ');\n"
    '\n'
    'INSERT INTO book (isbn, title, publisher_id, price, copies, status, added_on) VALUES\n'
    "    ('9786170000011', 'Кобзар', 2, 320.00, 5, 'active', '2025-01-15'),\n"
    "    ('9786170000028', 'Тіні забутих предків', 2, 210.50, 0, 'active', '2025-02-10'),\n"
    "    ('9786170000035', 'Захар Беркут', 1, 185.00, 3, 'active', '2025-02-20'),\n"
    "    ('9786170000042', 'Місто', 3, 260.00, 0, 'active', '2025-03-05'),\n"
    "    ('9786170000059', 'Intermezzo', 3, 150.00, 2, 'active', '2025-03-18'),\n"
    "    ('9786170000066', 'Лісова пісня', 1, 175.75, 7, 'active', '2025-04-02'),\n"
    "    ('9786170000073', 'Тигролови', 4, 230.00, 0, 'archived', '2025-04-22'),\n"
    "    ('9786170000080', 'Маруся', 4, 140.00, 4, 'active', '2025-05-11'),\n"
    "    ('9786170000097', 'Fata Morgana', 1, 199.90, 1, 'active', '2025-06-01'),\n"
    "    ('9786170000103', 'Кайдашева сім''я', 2, 165.00, 6, 'active', '2025-06-20'),\n"
    "    ('9786170000110', 'Хіба ревуть воли, як ясла повні?', 3, 410.00, 0, 'archived', '2025-07-07'),\n"
    "    ('9786170000127', 'Чорна рада', 4, 295.00, 2, 'active', '2025-07-30');\n"
    '\n'
    'INSERT INTO reader (full_name, email, registered_on, bonus) VALUES\n'
    "    ('Олена Шевченко', 'olena.s@example.com', '2025-01-10', 3),\n"
    "    ('Іван Коваль', 'ivan.k@example.com', '2025-01-22', 0),\n"
    "    ('Марія Бондар', 'maria.b@example.com', '2025-02-14', 2),\n"
    "    ('Петро Мельник', 'petro.m@example.com', '2025-03-03', 0),\n"
    "    ('Софія Ткачук', 'sofia.t@example.com', '2025-03-29', 5),\n"
    "    ('Андрій Кравець', 'andrii.k@example.com', '2025-04-17', 1),\n"
    "    ('Наталія Лисенко', 'natalia.l@example.com', '2025-05-05', 0),\n"
    "    ('Дмитро Гончар', 'dmytro.h@example.com', '2025-05-26', 4),\n"
    "    ('Юлія Пономаренко', 'yulia.p@example.com', '2025-06-09', 6);\n"
    '\n'
    'INSERT INTO loan (reader_id, book_id, copies, loaned_on, returned_on) VALUES\n'
    "    (1, 1, 1, '2025-02-01', '2025-02-15'),\n"
    "    (1, 3, 1, '2025-03-01', '2025-03-20'),\n"
    "    (2, 6, 1, '2025-03-10', NULL),\n"
    "    (3, 1, 1, '2025-03-15', '2025-04-01'),\n"
    "    (3, 8, 2, '2025-04-02', '2025-04-20'),\n"
    "    (4, 3, 1, '2025-04-05', NULL),\n"
    "    (4, 10, 1, '2025-04-18', '2025-05-02'),\n"
    "    (5, 7, 1, '2025-05-01', '2025-05-12'),\n"
    "    (5, 11, 1, '2025-05-03', NULL),\n"
    "    (6, 2, 1, '2025-05-20', NULL),\n"
    "    (6, 12, 1, '2025-06-01', '2025-06-15'),\n"
    "    (7, 6, 2, '2025-06-10', NULL),\n"
    "    (7, 9, 1, '2025-06-12', '2025-06-28'),\n"
    "    (8, 5, 1, '2025-06-20', NULL),\n"
    "    (8, 8, 1, '2025-07-01', NULL),\n"
    "    (1, 10, 1, '2025-07-05', NULL);\n"
    '\n'
    'INSERT INTO price_list (isbn, new_price) VALUES\n'
    "    ('9786170000011', 340.00),\n"
    "    ('9786170000035', 175.00),\n"
    "    ('9786170000042', 275.00),\n"
    "    ('9786170000080', 140.00),\n"
    "    ('9786170009999', 100.00);\n"
    '\n'
    'INSERT INTO supplier_feed (isbn, title, publisher_id, price, copies) VALUES\n'
    "    ('9786170000028', 'Тіні забутих предків', 2, 225.00, 10),\n"
    "    ('9786170000042', 'Місто', 3, 270.00, 5),\n"
    "    ('9786170000059', 'Intermezzo', 3, 155.00, 3),\n"
    "    ('9786170000073', 'Тигролови', 4, 240.00, 6),\n"
    "    ('9786170000200', 'Лис Микита', 1, 120.00, 10),\n"
    "    ('9786170000217', 'Дім з химерами', 3, 275.50, 4);\n"
    '\n'
    'INSERT INTO catalog_sync (isbn, title, publisher_id, price, copies) VALUES\n'
    "    ('9786170000011', 'Кобзар', 2, 320.00, 5),\n"
    "    ('9786170000028', 'Тіні забутих предків', 2, 230.00, 4),\n"
    "    ('9786170000035', 'Захар Беркут', 1, 185.00, 1),\n"
    "    ('9786170000066', 'Лісова пісня', 1, 180.00, 7),\n"
    "    ('9786170000103', 'Кайдашева сім''я', 2, 165.00, 6),\n"
    "    ('9786170000110', 'Хіба ревуть воли, як ясла повні?', 3, 405.00, 3),\n"
    "    ('9786170000127', 'Чорна рада', 4, 295.00, 2),\n"
    "    ('9786170000301', 'Енеїда', 2, 260.00, 5),\n"
    "    ('9786170000318', 'Гайдамаки', 1, 150.00, 8);\n"
    '\n'
    'INSERT INTO audit_log (note) VALUES\n'
    "    ('Початкове завантаження каталогу'),\n"
    "    ('Перевірка ISBN'),\n"
    "    ('Імпорт читачів'),\n"
    "    ('Резервна копія');\n",
 2: '-- Схема набору 2: Магазин. PostgreSQL 18.\n'
    '-- Файл створює таблиці й наповнює їх початковими даними. Виконуйте його в ПОРОЖНІЙ схемі.\n'
    '\n'
    'CREATE TABLE category (\n'
    '    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    name varchar(100) NOT NULL UNIQUE,\n'
    '    section varchar(60)\n'
    ');\n'
    '\n'
    'CREATE TABLE product (\n'
    '    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    sku   varchar(12) NOT NULL UNIQUE,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    category_id    integer NOT NULL REFERENCES category (id),\n'
    '    price  numeric(10,2) NOT NULL CHECK (price >= 0),\n'
    '    stock    integer NOT NULL DEFAULT 0 CHECK (stock >= 0),\n'
    "    status varchar(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),\n"
    '    added_on  date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE customer (\n'
    '    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    full_name  varchar(150) NOT NULL,\n'
    '    email  varchar(120) NOT NULL UNIQUE,\n'
    '    registered_on date NOT NULL DEFAULT current_date,\n'
    '    bonus integer NOT NULL DEFAULT 0\n'
    ');\n'
    '\n'
    'CREATE TABLE purchase (\n'
    '    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    customer_id integer NOT NULL REFERENCES customer (id),\n'
    '    product_id   integer NOT NULL REFERENCES product (id),\n'
    '    quantity    integer NOT NULL DEFAULT 1 CHECK (quantity > 0),\n'
    '    ordered_on   date NOT NULL,\n'
    '    shipped_on date\n'
    ');\n'
    '\n'
    'CREATE TABLE product_archive (\n'
    '    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    product_id    integer NOT NULL,\n'
    '    sku      varchar(12) NOT NULL,\n'
    '    title     varchar(200) NOT NULL,\n'
    '    price     numeric(10,2) NOT NULL,\n'
    '    note        varchar(100) NOT NULL,\n'
    '    archived_on date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE purchase_archive (\n'
    '    id        integer PRIMARY KEY,\n'
    '    customer_id integer NOT NULL,\n'
    '    product_id   integer NOT NULL,\n'
    '    quantity    integer NOT NULL,\n'
    '    ordered_on   date NOT NULL,\n'
    '    shipped_on date,\n'
    '    moved_on  date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE price_list (\n'
    '    sku    varchar(12) PRIMARY KEY,\n'
    '    new_price numeric(10,2) NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE supplier_feed (\n'
    '    sku   varchar(12) PRIMARY KEY,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    category_id    integer NOT NULL,\n'
    '    price  numeric(10,2) NOT NULL,\n'
    '    stock    integer NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE catalog_sync (\n'
    '    sku   varchar(12) PRIMARY KEY,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    category_id    integer NOT NULL,\n'
    '    price  numeric(10,2) NOT NULL,\n'
    '    stock    integer NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE audit_log (\n'
    '    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    note      varchar(200) NOT NULL,\n'
    '    logged_at timestamptz NOT NULL DEFAULT now()\n'
    ');\n'
    '\n'
    'CREATE TABLE stg_product (\n'
    '    sku   text,\n'
    '    title  text,\n'
    '    category_id    text,\n'
    '    price  text,\n'
    '    stock    text,\n'
    '    added_on  text\n'
    ');\n'
    '\n'
    '-- Початкові дані\n'
    '\n'
    'INSERT INTO category (name, section) VALUES\n'
    "    ('Напої', 'Бакалія'),\n"
    "    ('Молочні вироби', 'Холодильні'),\n"
    "    ('Хлібобулочні', 'Випічка'),\n"
    "    ('Побутова хімія', 'Непродовольчі');\n"
    '\n'
    'INSERT INTO product (sku, title, category_id, price, stock, status, added_on) VALUES\n'
    "    ('SKU-0001', 'Кава зернова 1 кг', 1, 540.00, 12, 'active', '2025-01-12'),\n"
    "    ('SKU-0002', 'Чай чорний 100 пакетиків', 1, 98.50, 40, 'active', '2025-01-12'),\n"
    "    ('SKU-0003', 'Сік яблучний 1 л', 1, 54.90, 0, 'active', '2025-02-03'),\n"
    "    ('SKU-0004', 'Молоко 2.5% 900 мл', 2, 42.00, 25, 'active', '2025-02-03'),\n"
    "    ('SKU-0005', 'Йогурт натуральний', 2, 28.50, 3, 'active', '2025-02-20'),\n"
    "    ('SKU-0006', 'Сир кисломолочний', 2, 76.00, 0, 'active', '2025-03-08'),\n"
    "    ('SKU-0007', 'Хліб пшеничний', 3, 31.00, 18, 'active', '2025-03-08'),\n"
    "    ('SKU-0008', 'Багет французький', 3, 39.00, 2, 'active', '2025-04-01'),\n"
    "    ('SKU-0009', 'Пончик з кремом', 3, 24.50, 0, 'archived', '2025-04-01'),\n"
    "    ('SKU-0010', 'Порошок пральний 3 кг', 4, 289.00, 9, 'active', '2025-04-15'),\n"
    "    ('SKU-0011', 'Засіб для посуду', 4, 67.40, 15, 'active', '2025-05-06'),\n"
    "    ('SKU-0012', 'Губки кухонні 5 шт.', 4, 35.00, 0, 'archived', '2025-05-06');\n"
    '\n'
    'INSERT INTO customer (full_name, email, registered_on, bonus) VALUES\n'
    "    ('Оксана Мороз', 'oksana.m@example.com', '2025-01-05', 10),\n"
    "    ('Богдан Савчук', 'bohdan.s@example.com', '2025-01-30', 0),\n"
    "    ('Галина Петренко', 'halyna.p@example.com', '2025-02-18', 4),\n"
    "    ('Левко Радченко', 'levko.r@example.com', '2025-03-11', 0),\n"
    "    ('Катерина Іваненко', 'kateryna.i@example.com', '2025-04-04', 7),\n"
    "    ('Максим Захарчук', 'maksym.z@example.com', '2025-04-29', 2),\n"
    "    ('Ірина Остапчук', 'iryna.o@example.com', '2025-05-21', 0),\n"
    "    ('Тимур Гнатюк', 'tymur.h@example.com', '2025-06-12', 5),\n"
    "    ('Олеся Крюк', 'olesia.k@example.com', '2025-07-01', 6);\n"
    '\n'
    'INSERT INTO purchase (customer_id, product_id, quantity, ordered_on, shipped_on) VALUES\n'
    "    (1, 1, 2, '2025-02-01', '2025-02-03'),\n"
    "    (1, 4, 3, '2025-02-15', '2025-02-16'),\n"
    "    (2, 2, 1, '2025-03-02', '2025-03-04'),\n"
    "    (2, 7, 2, '2025-03-20', '2025-03-21'),\n"
    "    (3, 5, 4, '2025-04-02', '2025-04-03'),\n"
    "    (3, 9, 1, '2025-04-10', '2025-04-12'),\n"
    "    (4, 10, 1, '2025-04-25', '2025-04-27'),\n"
    "    (4, 11, 2, '2025-05-06', NULL),\n"
    "    (5, 3, 3, '2025-05-18', '2025-05-20'),\n"
    "    (5, 12, 2, '2025-06-01', '2025-06-03'),\n"
    "    (6, 8, 1, '2025-06-14', NULL),\n"
    "    (6, 1, 1, '2025-06-28', '2025-06-30'),\n"
    "    (7, 2, 5, '2025-07-03', '2025-07-05'),\n"
    "    (7, 9, 2, '2025-07-19', NULL),\n"
    "    (8, 6, 1, '2025-08-01', '2025-08-02'),\n"
    "    (8, 10, 2, '2025-08-15', NULL);\n"
    '\n'
    'INSERT INTO price_list (sku, new_price) VALUES\n'
    "    ('SKU-0002', 105.00),\n"
    "    ('SKU-0005', 29.90),\n"
    "    ('SKU-0007', 33.50),\n"
    "    ('SKU-0010', 279.00),\n"
    "    ('SKU-9999', 10.00);\n"
    '\n'
    'INSERT INTO supplier_feed (sku, title, category_id, price, stock) VALUES\n'
    "    ('SKU-0001', 'Кава зернова 1 кг', 1, 520.00, 20),\n"
    "    ('SKU-0003', 'Сік яблучний 1 л', 1, 59.00, 30),\n"
    "    ('SKU-0006', 'Сир кисломолочний', 2, 72.00, 15),\n"
    "    ('SKU-0008', 'Багет французький', 3, 39.00, 10),\n"
    "    ('SKU-0101', 'Йогурт грецький', 2, 38.50, 40),\n"
    "    ('SKU-0102', 'Кефір 1%', 2, 36.00, 25);\n"
    '\n'
    'INSERT INTO catalog_sync (sku, title, category_id, price, stock) VALUES\n'
    "    ('SKU-0001', 'Кава зернова 1 кг', 1, 540.00, 12),\n"
    "    ('SKU-0002', 'Чай чорний 100 пакетиків', 1, 102.00, 40),\n"
    "    ('SKU-0004', 'Молоко 2.5% 900 мл', 2, 42.00, 30),\n"
    "    ('SKU-0005', 'Йогурт натуральний', 2, 28.50, 3),\n"
    "    ('SKU-0007', 'Хліб пшеничний', 3, 33.00, 18),\n"
    "    ('SKU-0008', 'Багет французький', 3, 39.00, 6),\n"
    "    ('SKU-0010', 'Порошок пральний 3 кг', 4, 289.00, 9),\n"
    "    ('SKU-0011', 'Засіб для посуду', 4, 70.00, 20),\n"
    "    ('SKU-0201', 'Мед липовий 500 г', 3, 210.00, 7),\n"
    "    ('SKU-0202', 'Печиво вівсяне', 3, 45.00, 22);\n"
    '\n'
    'INSERT INTO audit_log (note) VALUES\n'
    "    ('Початкове завантаження асортименту'),\n"
    "    ('Перевірка цін'),\n"
    "    ('Імпорт покупців'),\n"
    "    ('Резервна копія');\n",
 3: '-- Схема набору 3: Облік обладнання. PostgreSQL 18.\n'
    '-- Файл створює таблиці й наповнює їх початковими даними. Виконуйте його в ПОРОЖНІЙ схемі.\n'
    '\n'
    'CREATE TABLE department (\n'
    '    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    name varchar(100) NOT NULL UNIQUE,\n'
    '    room varchar(60)\n'
    ');\n'
    '\n'
    'CREATE TABLE device (\n'
    '    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    inv_no   varchar(12) NOT NULL UNIQUE,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    department_id    integer NOT NULL REFERENCES department (id),\n'
    '    cost  numeric(10,2) NOT NULL CHECK (cost >= 0),\n'
    '    quantity    integer NOT NULL DEFAULT 0 CHECK (quantity >= 0),\n'
    "    status varchar(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),\n"
    '    added_on  date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE employee (\n'
    '    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    full_name  varchar(150) NOT NULL,\n'
    '    email  varchar(120) NOT NULL UNIQUE,\n'
    '    hired_on date NOT NULL DEFAULT current_date,\n'
    '    held integer NOT NULL DEFAULT 0\n'
    ');\n'
    '\n'
    'CREATE TABLE issue (\n'
    '    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    employee_id integer NOT NULL REFERENCES employee (id),\n'
    '    device_id   integer NOT NULL REFERENCES device (id),\n'
    '    quantity    integer NOT NULL DEFAULT 1 CHECK (quantity > 0),\n'
    '    issued_on   date NOT NULL,\n'
    '    returned_on date\n'
    ');\n'
    '\n'
    'CREATE TABLE device_archive (\n'
    '    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    device_id    integer NOT NULL,\n'
    '    inv_no      varchar(12) NOT NULL,\n'
    '    title     varchar(200) NOT NULL,\n'
    '    cost     numeric(10,2) NOT NULL,\n'
    '    note        varchar(100) NOT NULL,\n'
    '    archived_on date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE issue_archive (\n'
    '    id        integer PRIMARY KEY,\n'
    '    employee_id integer NOT NULL,\n'
    '    device_id   integer NOT NULL,\n'
    '    quantity    integer NOT NULL,\n'
    '    issued_on   date NOT NULL,\n'
    '    returned_on date,\n'
    '    moved_on  date NOT NULL DEFAULT current_date\n'
    ');\n'
    '\n'
    'CREATE TABLE price_list (\n'
    '    inv_no    varchar(12) PRIMARY KEY,\n'
    '    new_cost numeric(10,2) NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE supplier_feed (\n'
    '    inv_no   varchar(12) PRIMARY KEY,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    department_id    integer NOT NULL,\n'
    '    cost  numeric(10,2) NOT NULL,\n'
    '    quantity    integer NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE catalog_sync (\n'
    '    inv_no   varchar(12) PRIMARY KEY,\n'
    '    title  varchar(200) NOT NULL,\n'
    '    department_id    integer NOT NULL,\n'
    '    cost  numeric(10,2) NOT NULL,\n'
    '    quantity    integer NOT NULL\n'
    ');\n'
    '\n'
    'CREATE TABLE audit_log (\n'
    '    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n'
    '    note      varchar(200) NOT NULL,\n'
    '    logged_at timestamptz NOT NULL DEFAULT now()\n'
    ');\n'
    '\n'
    'CREATE TABLE stg_device (\n'
    '    inv_no   text,\n'
    '    title  text,\n'
    '    department_id    text,\n'
    '    cost  text,\n'
    '    quantity    text,\n'
    '    added_on  text\n'
    ');\n'
    '\n'
    '-- Початкові дані\n'
    '\n'
    'INSERT INTO department (name, room) VALUES\n'
    "    ('Інформатика', 'каб. 301'),\n"
    "    ('Фізика', 'каб. 112'),\n"
    "    ('Бібліотека', 'каб. 105'),\n"
    "    ('Майстерня', 'каб. 009');\n"
    '\n'
    'INSERT INTO device (inv_no, title, department_id, cost, quantity, status, added_on) VALUES\n'
    "    ('INV-1001', 'Ноутбук Lenovo ThinkPad', 1, 28500.00, 6, 'active', '2025-01-20'),\n"
    "    ('INV-1002', 'Проєктор Epson', 1, 17900.00, 3, 'active', '2025-01-20'),\n"
    "    ('INV-1003', 'Маршрутизатор MikroTik', 1, 3200.00, 0, 'active', '2025-02-14'),\n"
    "    ('INV-1004', 'Осцилограф цифровий', 2, 12400.00, 2, 'active', '2025-02-14'),\n"
    "    ('INV-1005', 'Набір магнітів', 2, 640.00, 10, 'active', '2025-03-01'),\n"
    "    ('INV-1006', 'Мультиметр', 2, 890.50, 0, 'active', '2025-03-01'),\n"
    "    ('INV-1007', 'Принтер лазерний', 3, 6700.00, 1, 'active', '2025-03-25'),\n"
    "    ('INV-1008', 'Сканер штрихкодів', 3, 2150.00, 2, 'active', '2025-04-09'),\n"
    "    ('INV-1009', 'Монітор Samsung', 3, 2400.00, 0, 'archived', '2025-04-09'),\n"
    "    ('INV-1010', 'Верстат свердлильний', 4, 15800.00, 1, 'active', '2025-05-12'),\n"
    "    ('INV-1011', 'Набір викруток', 4, 420.00, 12, 'active', '2025-05-12'),\n"
    "    ('INV-1012', 'Паяльна станція', 4, 3650.00, 0, 'archived', '2025-06-02');\n"
    '\n'
    'INSERT INTO employee (full_name, email, hired_on, held) VALUES\n'
    "    ('Руслан Дяченко', 'ruslan.d@example.com', '2024-09-02', 2),\n"
    "    ('Лілія Сорока', 'liliia.s@example.com', '2024-10-14', 1),\n"
    "    ('Валентин Герасименко', 'valentyn.h@example.com', '2024-11-25', 0),\n"
    "    ('Алла Шаповал', 'alla.s@example.com', '2025-01-13', 3),\n"
    "    ('Єгор Приходько', 'yehor.p@example.com', '2025-02-17', 0),\n"
    "    ('Ніна Лук''яненко', 'nina.l@example.com', '2025-03-24', 4),\n"
    "    ('Станіслав Мазур', 'stanislav.m@example.com', '2025-04-28', 1),\n"
    "    ('Віра Павленко', 'vira.p@example.com', '2025-05-19', 0),\n"
    "    ('Артем Бойко', 'artem.b@example.com', '2025-06-16', 5);\n"
    '\n'
    'INSERT INTO issue (employee_id, device_id, quantity, issued_on, returned_on) VALUES\n'
    "    (1, 1, 1, '2025-02-03', '2025-05-30'),\n"
    "    (1, 5, 2, '2025-03-10', '2025-03-24'),\n"
    "    (2, 2, 1, '2025-03-12', NULL),\n"
    "    (2, 4, 1, '2025-03-15', '2025-04-15'),\n"
    "    (3, 8, 1, '2025-04-14', '2025-06-10'),\n"
    "    (3, 9, 1, '2025-04-20', '2025-05-20'),\n"
    "    (4, 10, 1, '2025-05-15', NULL),\n"
    "    (4, 11, 3, '2025-05-20', '2025-06-05'),\n"
    "    (5, 12, 1, '2025-06-03', '2025-06-30'),\n"
    "    (5, 7, 1, '2025-06-10', NULL),\n"
    "    (6, 1, 2, '2025-06-18', NULL),\n"
    "    (6, 9, 1, '2025-06-25', NULL),\n"
    "    (7, 5, 4, '2025-07-01', '2025-07-15'),\n"
    "    (7, 2, 1, '2025-07-09', '2025-08-01'),\n"
    "    (8, 6, 1, '2025-07-20', NULL),\n"
    "    (8, 11, 2, '2025-08-04', NULL);\n"
    '\n'
    'INSERT INTO price_list (inv_no, new_cost) VALUES\n'
    "    ('INV-1001', 27990.00),\n"
    "    ('INV-1004', 12900.00),\n"
    "    ('INV-1008', 2150.00),\n"
    "    ('INV-1011', 450.00),\n"
    "    ('INV-9999', 100.00);\n"
    '\n'
    'INSERT INTO supplier_feed (inv_no, title, department_id, cost, quantity) VALUES\n'
    "    ('INV-1001', 'Ноутбук Lenovo ThinkPad', 1, 27500.00, 8),\n"
    "    ('INV-1003', 'Маршрутизатор MikroTik', 1, 3200.00, 4),\n"
    "    ('INV-1006', 'Мультиметр', 2, 860.00, 6),\n"
    "    ('INV-1011', 'Набір викруток', 4, 420.00, 12),\n"
    "    ('INV-1101', 'Миша бездротова', 1, 450.00, 20),\n"
    "    ('INV-1102', 'Лампа настільна', 3, 380.00, 9);\n"
    '\n'
    'INSERT INTO catalog_sync (inv_no, title, department_id, cost, quantity) VALUES\n'
    "    ('INV-1001', 'Ноутбук Lenovo ThinkPad', 1, 28500.00, 6),\n"
    "    ('INV-1002', 'Проєктор Epson', 1, 18200.00, 3),\n"
    "    ('INV-1004', 'Осцилограф цифровий', 2, 12400.00, 3),\n"
    "    ('INV-1005', 'Набір магнітів', 2, 640.00, 10),\n"
    "    ('INV-1007', 'Принтер лазерний', 3, 6900.00, 2),\n"
    "    ('INV-1008', 'Сканер штрихкодів', 3, 2150.00, 2),\n"
    "    ('INV-1010', 'Верстат свердлильний', 4, 15800.00, 1),\n"
    "    ('INV-1011', 'Набір викруток', 4, 430.00, 12),\n"
    "    ('INV-1201', 'Крокодили з''єднувальні', 2, 95.00, 30);\n"
    '\n'
    'INSERT INTO audit_log (note) VALUES\n'
    "    ('Початкова інвентаризація'),\n"
    "    ('Перевірка інвентарних номерів'),\n"
    "    ('Імпорт працівників'),\n"
    "    ('Резервна копія');\n"}
