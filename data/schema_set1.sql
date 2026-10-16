-- Схема набору 1: Бібліотека. PostgreSQL 18.
-- Файл створює таблиці й наповнює їх початковими даними. Виконуйте його в ПОРОЖНІЙ схемі.

CREATE TABLE publisher (
    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    city varchar(60)
);

CREATE TABLE book (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    isbn   char(13) NOT NULL UNIQUE,
    title  varchar(200) NOT NULL,
    publisher_id    integer NOT NULL REFERENCES publisher (id),
    price  numeric(10,2) NOT NULL CHECK (price >= 0),
    copies    integer NOT NULL DEFAULT 0 CHECK (copies >= 0),
    status varchar(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),
    added_on  date NOT NULL DEFAULT current_date
);

CREATE TABLE reader (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name  varchar(150) NOT NULL,
    email  varchar(120) NOT NULL UNIQUE,
    registered_on date NOT NULL DEFAULT current_date,
    bonus integer NOT NULL DEFAULT 0
);

CREATE TABLE loan (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reader_id integer NOT NULL REFERENCES reader (id),
    book_id   integer NOT NULL REFERENCES book (id),
    copies    integer NOT NULL DEFAULT 1 CHECK (copies > 0),
    loaned_on   date NOT NULL,
    returned_on date
);

CREATE TABLE book_archive (
    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id    integer NOT NULL,
    isbn      char(13) NOT NULL,
    title     varchar(200) NOT NULL,
    price     numeric(10,2) NOT NULL,
    note        varchar(100) NOT NULL,
    archived_on date NOT NULL DEFAULT current_date
);

CREATE TABLE loan_archive (
    id        integer PRIMARY KEY,
    reader_id integer NOT NULL,
    book_id   integer NOT NULL,
    copies    integer NOT NULL,
    loaned_on   date NOT NULL,
    returned_on date,
    moved_on  date NOT NULL DEFAULT current_date
);

CREATE TABLE price_list (
    isbn    char(13) PRIMARY KEY,
    new_price numeric(10,2) NOT NULL
);

CREATE TABLE supplier_feed (
    isbn   char(13) PRIMARY KEY,
    title  varchar(200) NOT NULL,
    publisher_id    integer NOT NULL,
    price  numeric(10,2) NOT NULL,
    copies    integer NOT NULL
);

CREATE TABLE catalog_sync (
    isbn   char(13) PRIMARY KEY,
    title  varchar(200) NOT NULL,
    publisher_id    integer NOT NULL,
    price  numeric(10,2) NOT NULL,
    copies    integer NOT NULL
);

CREATE TABLE audit_log (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    note      varchar(200) NOT NULL,
    logged_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE stg_book (
    isbn   text,
    title  text,
    publisher_id    text,
    price  text,
    copies    text,
    added_on  text
);

-- Початкові дані

INSERT INTO publisher (name, city) VALUES
    ('Фабула', 'Харків'),
    ('Старий Лев', 'Львів'),
    ('Ранок', 'Харків'),
    ('Основи', 'Київ');

INSERT INTO book (isbn, title, publisher_id, price, copies, status, added_on) VALUES
    ('9786170000011', 'Кобзар', 2, 320.00, 5, 'active', '2025-01-15'),
    ('9786170000028', 'Тіні забутих предків', 2, 210.50, 0, 'active', '2025-02-10'),
    ('9786170000035', 'Захар Беркут', 1, 185.00, 3, 'active', '2025-02-20'),
    ('9786170000042', 'Місто', 3, 260.00, 0, 'active', '2025-03-05'),
    ('9786170000059', 'Intermezzo', 3, 150.00, 2, 'active', '2025-03-18'),
    ('9786170000066', 'Лісова пісня', 1, 175.75, 7, 'active', '2025-04-02'),
    ('9786170000073', 'Тигролови', 4, 230.00, 0, 'archived', '2025-04-22'),
    ('9786170000080', 'Маруся', 4, 140.00, 4, 'active', '2025-05-11'),
    ('9786170000097', 'Fata Morgana', 1, 199.90, 1, 'active', '2025-06-01'),
    ('9786170000103', 'Кайдашева сім''я', 2, 165.00, 6, 'active', '2025-06-20'),
    ('9786170000110', 'Хіба ревуть воли, як ясла повні?', 3, 410.00, 0, 'archived', '2025-07-07'),
    ('9786170000127', 'Чорна рада', 4, 295.00, 2, 'active', '2025-07-30');

INSERT INTO reader (full_name, email, registered_on, bonus) VALUES
    ('Олена Шевченко', 'olena.s@example.com', '2025-01-10', 3),
    ('Іван Коваль', 'ivan.k@example.com', '2025-01-22', 0),
    ('Марія Бондар', 'maria.b@example.com', '2025-02-14', 2),
    ('Петро Мельник', 'petro.m@example.com', '2025-03-03', 0),
    ('Софія Ткачук', 'sofia.t@example.com', '2025-03-29', 5),
    ('Андрій Кравець', 'andrii.k@example.com', '2025-04-17', 1),
    ('Наталія Лисенко', 'natalia.l@example.com', '2025-05-05', 0),
    ('Дмитро Гончар', 'dmytro.h@example.com', '2025-05-26', 4),
    ('Юлія Пономаренко', 'yulia.p@example.com', '2025-06-09', 6);

INSERT INTO loan (reader_id, book_id, copies, loaned_on, returned_on) VALUES
    (1, 1, 1, '2025-02-01', '2025-02-15'),
    (1, 3, 1, '2025-03-01', '2025-03-20'),
    (2, 6, 1, '2025-03-10', NULL),
    (3, 1, 1, '2025-03-15', '2025-04-01'),
    (3, 8, 2, '2025-04-02', '2025-04-20'),
    (4, 3, 1, '2025-04-05', NULL),
    (4, 10, 1, '2025-04-18', '2025-05-02'),
    (5, 7, 1, '2025-05-01', '2025-05-12'),
    (5, 11, 1, '2025-05-03', NULL),
    (6, 2, 1, '2025-05-20', NULL),
    (6, 12, 1, '2025-06-01', '2025-06-15'),
    (7, 6, 2, '2025-06-10', NULL),
    (7, 9, 1, '2025-06-12', '2025-06-28'),
    (8, 5, 1, '2025-06-20', NULL),
    (8, 8, 1, '2025-07-01', NULL),
    (1, 10, 1, '2025-07-05', NULL);

INSERT INTO price_list (isbn, new_price) VALUES
    ('9786170000011', 340.00),
    ('9786170000035', 175.00),
    ('9786170000042', 275.00),
    ('9786170000080', 140.00),
    ('9786170009999', 100.00);

INSERT INTO supplier_feed (isbn, title, publisher_id, price, copies) VALUES
    ('9786170000028', 'Тіні забутих предків', 2, 225.00, 10),
    ('9786170000042', 'Місто', 3, 270.00, 5),
    ('9786170000059', 'Intermezzo', 3, 155.00, 3),
    ('9786170000073', 'Тигролови', 4, 240.00, 6),
    ('9786170000200', 'Лис Микита', 1, 120.00, 10),
    ('9786170000217', 'Дім з химерами', 3, 275.50, 4);

INSERT INTO catalog_sync (isbn, title, publisher_id, price, copies) VALUES
    ('9786170000011', 'Кобзар', 2, 320.00, 5),
    ('9786170000028', 'Тіні забутих предків', 2, 230.00, 4),
    ('9786170000035', 'Захар Беркут', 1, 185.00, 1),
    ('9786170000066', 'Лісова пісня', 1, 180.00, 7),
    ('9786170000103', 'Кайдашева сім''я', 2, 165.00, 6),
    ('9786170000110', 'Хіба ревуть воли, як ясла повні?', 3, 405.00, 3),
    ('9786170000127', 'Чорна рада', 4, 295.00, 2),
    ('9786170000301', 'Енеїда', 2, 260.00, 5),
    ('9786170000318', 'Гайдамаки', 1, 150.00, 8);

INSERT INTO audit_log (note) VALUES
    ('Початкове завантаження каталогу'),
    ('Перевірка ISBN'),
    ('Імпорт читачів'),
    ('Резервна копія');
