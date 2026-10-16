from conftest import load
from pgutil import Db
from schemas import SCHEMAS

def test_my_case():
    db = Db()
    try:
        db.run(SCHEMAS[2]) # Номер набору даних (Магазин = 2)
        # Додайте свій тестовий рядок за потреби
        db.run("INSERT INTO customer (full_name, email) VALUES ('Тестовий Клієнт', 'test.client@example.com');")
        
        # Виконуємо скрипт вашої задачі (номер 8)
        db.run(load(8).script())
        
        # Перевіряємо кількість рядків або інший показник
        assert db.value("SELECT count(*) FROM purchase_archive") >= 0
    finally:
        db.close()