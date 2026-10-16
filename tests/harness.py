"""Виконання перевірок зі специфікацій (specs.py): стан таблиць після SQL-скрипта студента."""
import inspect
from decimal import Decimal

import pytest

import pgutil
from schemas import SCHEMAS

FUNCS = {9: ("copy_command", "finish_script")}


def fail(message):
    pytest.fail(message, pytrace=False)


def norm(value):
    if value is None:
        return None
    if isinstance(value, Decimal):
        return format(value, "f")
    return str(value)


def norm_rows(rows):
    return [tuple(norm(v) for v in row) for row in rows]


def call(mod, name, task, set_no):
    """Викликає функцію варіанта. Еталон приймає номер набору; студентська функція без параметрів
    працює для набору, що випливає з константи VARIANT."""
    fn = getattr(mod, name, None)
    if fn is None:
        fail(f"У файлі варіанта немає функції {name}()")
    if inspect.signature(fn).parameters:
        return fn(set_no)
    variant = getattr(mod, "VARIANT", 0)
    if not variant:
        fail("Змінну VARIANT не задано: впишіть номер свого варіанта (1-30) на початку файла")
    if (variant - 1) // 3 + 1 != task:
        fail(f"VARIANT = {variant} не відповідає задачі {task}: файл variant_{task:02d}.py призначений "
             f"для варіантів {3 * task - 2}-{3 * task}")
    if (variant - 1) % 3 + 1 != set_no:
        pytest.skip("перевірка іншого набору даних")
    try:
        return fn()
    except NotImplementedError:
        fail(f"Функція {name}() ще не реалізована (NotImplementedError)")


def need_text(value, name):
    if not isinstance(value, str) or not value.strip():
        fail(f"{name}() має повертати непорожній рядок з SQL")
    return value


def run_script(db, sql, expect_error):
    try:
        db.run(sql)
    except pgutil.ScriptError as error:
        if expect_error and error.state == expect_error:
            return
        if expect_error:
            fail(f"Очікувалась помилка зі станом {expect_error} (RAISE EXCEPTION), отримано: {error}")
        fail(f"SQL-скрипт завершився помилкою {error}")
    if expect_error:
        fail(f"Очікувалась помилка {expect_error}: скрипт мав зупинитися через неочікувану кількість змінених рядків")


def run_case(db, mod, task, set_no, spec, chk):
    db.run(SCHEMAS[set_no])
    for sql in chk["setup"]:
        db.run(sql)
    if task == 9:
        cmd = need_text(call(mod, "copy_command", task, set_no), "copy_command")
        if "FROM STDIN" not in cmd.upper():
            fail("Команда COPY має читати дані зі стандартного входу: COPY таблиця FROM STDIN WITH (...)")
        try:
            db.copy_in(cmd, spec["csv"])
        except pgutil.ScriptError as error:
            fail(f"COPY завершилась помилкою {error}")
        if chk["stage"] == "full":
            run_script(db, need_text(call(mod, "finish_script", task, set_no), "finish_script"), None)
    else:
        run_script(db, need_text(call(mod, "script", task, set_no), "script"), chk["error"])
    for sql in chk["after"]:
        db.run(sql)
    got = norm_rows(db.rows(chk["sql"]))
    want = norm_rows(chk["expect"])
    if not chk["ordered"]:
        got, want = sorted(got, key=repr), sorted(want, key=repr)
    if got != want:
        missing = [r for r in want if r not in got]
        extra = [r for r in got if r not in want]
        lines = [f"Перевірка «{chk['id']}»: очікувалось рядків {len(want)}, отримано {len(got)}."]
        if missing:
            lines.append("Бракує: " + "; ".join(map(str, missing[:3])) + (" ..." if len(missing) > 3 else ""))
        if extra:
            lines.append("Зайві або інші: " + "; ".join(map(str, extra[:3])) + (" ..." if len(extra) > 3 else ""))
        lines.append("Запит перевірки: " + chk["sql"])
        fail("\n".join(lines))
