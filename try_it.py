"""Ручний прогін вашого розв'язку без тестів.

Використання:  python try_it.py <номер_задачі> [таблиця ...]
Скрипт створює тимчасову схему, завантажує схему й дані вашого набору (за VARIANT у файлі variants/variant_NN.py),
виконує вашу функцію (для задачі 9 ще й завантажує CSV) і друкує вміст зазначених таблиць
(без назв таблиць друкує кількість рядків у всіх таблицях). Тимчасова схема видаляється наприкінці.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tests"))

import pgutil  # noqa: E402
from conftest import load  # noqa: E402
from schemas import SCHEMAS  # noqa: E402


def main():
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print(__doc__)
        return 1
    task = int(sys.argv[1])
    mod = load(task)
    variant = getattr(mod, "VARIANT", 0)
    if not variant or (variant - 1) // 3 + 1 != task:
        print(f"Вкажіть у variant_{task:02d}.py змінну VARIANT зі значенням {3 * task - 2}-{3 * task}.")
        return 1
    set_no = (variant - 1) % 3 + 1
    db = pgutil.Db()
    try:
        db.run(SCHEMAS[set_no])
        if task == 9:
            csv_text = (ROOT / "data" / f"import_set{set_no}.csv").read_text(encoding="utf-8")
            db.copy_in(mod.copy_command(), csv_text)
            db.run(mod.finish_script())
        else:
            db.run(mod.script())
        names = sys.argv[2:] or [r[0] for r in db.rows(
            "SELECT relname FROM pg_class WHERE relnamespace = current_schema()::regnamespace AND relkind = 'r' ORDER BY 1")]
        for name in names:
            rows = db.rows(f"SELECT * FROM {name} ORDER BY 1")
            print(f"--- {name}: {len(rows)} рядків")
            if len(sys.argv) > 2:
                for row in rows:
                    print(row)
    except pgutil.ScriptError as error:
        print("Помилка SQL:", error)
        return 1
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
