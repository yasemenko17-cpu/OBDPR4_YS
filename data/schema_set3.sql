-- Схема набору 3: Облік обладнання. PostgreSQL 18.
-- Файл створює таблиці й наповнює їх початковими даними. Виконуйте його в ПОРОЖНІЙ схемі.

CREATE TABLE department (
    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    room varchar(60)
);

CREATE TABLE device (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    inv_no   varchar(12) NOT NULL UNIQUE,
    title  varchar(200) NOT NULL,
    department_id    integer NOT NULL REFERENCES department (id),
    cost  numeric(10,2) NOT NULL CHECK (cost >= 0),
    quantity    integer NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    status varchar(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),
    added_on  date NOT NULL DEFAULT current_date
);

CREATE TABLE employee (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name  varchar(150) NOT NULL,
    email  varchar(120) NOT NULL UNIQUE,
    hired_on date NOT NULL DEFAULT current_date,
    held integer NOT NULL DEFAULT 0
);

CREATE TABLE issue (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id integer NOT NULL REFERENCES employee (id),
    device_id   integer NOT NULL REFERENCES device (id),
    quantity    integer NOT NULL DEFAULT 1 CHECK (quantity > 0),
    issued_on   date NOT NULL,
    returned_on date
);

CREATE TABLE device_archive (
    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_id    integer NOT NULL,
    inv_no      varchar(12) NOT NULL,
    title     varchar(200) NOT NULL,
    cost     numeric(10,2) NOT NULL,
    note        varchar(100) NOT NULL,
    archived_on date NOT NULL DEFAULT current_date
);

CREATE TABLE issue_archive (
    id        integer PRIMARY KEY,
    employee_id integer NOT NULL,
    device_id   integer NOT NULL,
    quantity    integer NOT NULL,
    issued_on   date NOT NULL,
    returned_on date,
    moved_on  date NOT NULL DEFAULT current_date
);

CREATE TABLE price_list (
    inv_no    varchar(12) PRIMARY KEY,
    new_cost numeric(10,2) NOT NULL
);

CREATE TABLE supplier_feed (
    inv_no   varchar(12) PRIMARY KEY,
    title  varchar(200) NOT NULL,
    department_id    integer NOT NULL,
    cost  numeric(10,2) NOT NULL,
    quantity    integer NOT NULL
);

CREATE TABLE catalog_sync (
    inv_no   varchar(12) PRIMARY KEY,
    title  varchar(200) NOT NULL,
    department_id    integer NOT NULL,
    cost  numeric(10,2) NOT NULL,
    quantity    integer NOT NULL
);

CREATE TABLE audit_log (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note      varchar(200) NOT NULL,
    logged_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE stg_device (
    inv_no   text,
    title  text,
    department_id    text,
    cost  text,
    quantity    text,
    added_on  text
);

-- Початкові дані

INSERT INTO department (name, room) VALUES
    ('Інформатика', 'каб. 301'),
    ('Фізика', 'каб. 112'),
    ('Бібліотека', 'каб. 105'),
    ('Майстерня', 'каб. 009');

INSERT INTO device (inv_no, title, department_id, cost, quantity, status, added_on) VALUES
    ('INV-1001', 'Ноутбук Lenovo ThinkPad', 1, 28500.00, 6, 'active', '2025-01-20'),
    ('INV-1002', 'Проєктор Epson', 1, 17900.00, 3, 'active', '2025-01-20'),
    ('INV-1003', 'Маршрутизатор MikroTik', 1, 3200.00, 0, 'active', '2025-02-14'),
    ('INV-1004', 'Осцилограф цифровий', 2, 12400.00, 2, 'active', '2025-02-14'),
    ('INV-1005', 'Набір магнітів', 2, 640.00, 10, 'active', '2025-03-01'),
    ('INV-1006', 'Мультиметр', 2, 890.50, 0, 'active', '2025-03-01'),
    ('INV-1007', 'Принтер лазерний', 3, 6700.00, 1, 'active', '2025-03-25'),
    ('INV-1008', 'Сканер штрихкодів', 3, 2150.00, 2, 'active', '2025-04-09'),
    ('INV-1009', 'Монітор Samsung', 3, 2400.00, 0, 'archived', '2025-04-09'),
    ('INV-1010', 'Верстат свердлильний', 4, 15800.00, 1, 'active', '2025-05-12'),
    ('INV-1011', 'Набір викруток', 4, 420.00, 12, 'active', '2025-05-12'),
    ('INV-1012', 'Паяльна станція', 4, 3650.00, 0, 'archived', '2025-06-02');

INSERT INTO employee (full_name, email, hired_on, held) VALUES
    ('Руслан Дяченко', 'ruslan.d@example.com', '2024-09-02', 2),
    ('Лілія Сорока', 'liliia.s@example.com', '2024-10-14', 1),
    ('Валентин Герасименко', 'valentyn.h@example.com', '2024-11-25', 0),
    ('Алла Шаповал', 'alla.s@example.com', '2025-01-13', 3),
    ('Єгор Приходько', 'yehor.p@example.com', '2025-02-17', 0),
    ('Ніна Лук''яненко', 'nina.l@example.com', '2025-03-24', 4),
    ('Станіслав Мазур', 'stanislav.m@example.com', '2025-04-28', 1),
    ('Віра Павленко', 'vira.p@example.com', '2025-05-19', 0),
    ('Артем Бойко', 'artem.b@example.com', '2025-06-16', 5);

INSERT INTO issue (employee_id, device_id, quantity, issued_on, returned_on) VALUES
    (1, 1, 1, '2025-02-03', '2025-05-30'),
    (1, 5, 2, '2025-03-10', '2025-03-24'),
    (2, 2, 1, '2025-03-12', NULL),
    (2, 4, 1, '2025-03-15', '2025-04-15'),
    (3, 8, 1, '2025-04-14', '2025-06-10'),
    (3, 9, 1, '2025-04-20', '2025-05-20'),
    (4, 10, 1, '2025-05-15', NULL),
    (4, 11, 3, '2025-05-20', '2025-06-05'),
    (5, 12, 1, '2025-06-03', '2025-06-30'),
    (5, 7, 1, '2025-06-10', NULL),
    (6, 1, 2, '2025-06-18', NULL),
    (6, 9, 1, '2025-06-25', NULL),
    (7, 5, 4, '2025-07-01', '2025-07-15'),
    (7, 2, 1, '2025-07-09', '2025-08-01'),
    (8, 6, 1, '2025-07-20', NULL),
    (8, 11, 2, '2025-08-04', NULL);

INSERT INTO price_list (inv_no, new_cost) VALUES
    ('INV-1001', 27990.00),
    ('INV-1004', 12900.00),
    ('INV-1008', 2150.00),
    ('INV-1011', 450.00),
    ('INV-9999', 100.00);

INSERT INTO supplier_feed (inv_no, title, department_id, cost, quantity) VALUES
    ('INV-1001', 'Ноутбук Lenovo ThinkPad', 1, 27500.00, 8),
    ('INV-1003', 'Маршрутизатор MikroTik', 1, 3200.00, 4),
    ('INV-1006', 'Мультиметр', 2, 860.00, 6),
    ('INV-1011', 'Набір викруток', 4, 420.00, 12),
    ('INV-1101', 'Миша бездротова', 1, 450.00, 20),
    ('INV-1102', 'Лампа настільна', 3, 380.00, 9);

INSERT INTO catalog_sync (inv_no, title, department_id, cost, quantity) VALUES
    ('INV-1001', 'Ноутбук Lenovo ThinkPad', 1, 28500.00, 6),
    ('INV-1002', 'Проєктор Epson', 1, 18200.00, 3),
    ('INV-1004', 'Осцилограф цифровий', 2, 12400.00, 3),
    ('INV-1005', 'Набір магнітів', 2, 640.00, 10),
    ('INV-1007', 'Принтер лазерний', 3, 6900.00, 2),
    ('INV-1008', 'Сканер штрихкодів', 3, 2150.00, 2),
    ('INV-1010', 'Верстат свердлильний', 4, 15800.00, 1),
    ('INV-1011', 'Набір викруток', 4, 430.00, 12),
    ('INV-1201', 'Крокодили з''єднувальні', 2, 95.00, 30);

INSERT INTO audit_log (note) VALUES
    ('Початкова інвентаризація'),
    ('Перевірка інвентарних номерів'),
    ('Імпорт працівників'),
    ('Резервна копія');
