"""Задания 1–6: UTF-8, encode/decode и read_bytes в encoding_lab."""

import argparse
from pathlib import Path
from main import checkpoint, inspect_encoding, write_utf8

STUDENT_TEXT = "Студент: Зыков Егор Тимурович.\nПрактическая работа по кодировкам текста.\n"
PROFILE_TEXT = "Имя: Зыков Егор Тимурович.\nГруппа: ИСиП-23-1.\nИзучаю хранение русского текста в файле.\n"


def main(pause=False):
    print("Рабочая папка:", Path.cwd())
    base = Path.cwd() / "encoding_lab"
    checkpoint("Перед созданием учебных файлов", pause)
    write_utf8(base / "texts/student.txt", STUDENT_TEXT)
    write_utf8(base / "texts/profile.txt", PROFILE_TEXT)
    checkpoint("student.txt и profile.txt записаны", pause)
    inspect_encoding(base / "texts/profile.txt", PROFILE_TEXT)
    checkpoint("profile.txt прочитан как текст и байты", pause)
    text = "Кодировка UTF-8 работает с кириллицей"
    data = text.encode("utf-8")
    print("Байты строки:", data)
    print("Восстановленная строка:", data.decode("utf-8"))
    print("Восстановленная строка совпадает:", data.decode("utf-8") == text)
    text = "Файл и кодировка"
    data = text.encode("utf-8")
    print("UTF-8:", data.decode("utf-8"))
    print("latin-1:", data.decode("latin-1"))
    print("UTF-8 совпадает:", data.decode("utf-8") == text)
    print("latin-1 совпадает:", data.decode("latin-1") == text)
    print("Байты одинаковы, но правила их преобразования в символы различаются.")
    checkpoint("encode/decode и сравнение кодировок завершены", pause)
    return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Учебные задания: кодировки")
    parser.add_argument("--pause", action="store_true")
    main(pause=parser.parse_args().pause)
