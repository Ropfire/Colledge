"""Практическая №5. Проверка кодировки. Зыков Е. Т., ИСиП-23-1."""

import argparse
from pathlib import Path

NOTE_TEXT = (
    "Автор заметки: Зыков Егор Тимурович.\n"
    "Группа ИСиП-23-1 изучает системное программирование.\n"
    "Сегодня проверяется сохранение русского текста в UTF-8.\n"
)
EXTRA_TEXT = "Байты хранят текст, а кодировка объясняет их значение.\n"


def checkpoint(message, pause=False):
    print("\n=== " + message + " ===", flush=True)
    if pause:
        input("Enter — продолжить: ")


def write_utf8(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)
    print("Файл записан в UTF-8:", path)
    print("Существует:", path.exists())


def read_utf8(path):
    with open(path, "r", encoding="utf-8", newline="\n") as file:
        return file.read()


def inspect_encoding(path, original):
    loaded = read_utf8(path)
    data = path.read_bytes()
    decoded_utf8 = data.decode("utf-8")
    decoded_latin1 = data.decode("latin-1")
    print("Прочитанный текст:\n" + loaded)
    print("Прочитанное совпадает с исходным:", loaded == original)
    print("Первые 20 байтов:", data[:20])
    print("Количество байтов:", len(data))
    print("UTF-8:\n" + decoded_utf8)
    print("latin-1:\n" + decoded_latin1)
    print("UTF-8 совпадает с исходным:", decoded_utf8 == original)
    print("latin-1 совпадает с исходным:", decoded_latin1 == original)
    print("UTF-8 восстанавливает кириллицу; latin-1 трактует каждый байт как отдельный символ.")
    return {
        "loaded": loaded, "data": data, "utf8": decoded_utf8,
        "latin1": decoded_latin1, "matches": loaded == original,
    }


def main(pause=False):
    print("Рабочая папка:", Path.cwd())
    base = Path.cwd() / "encoding_check"
    checkpoint("Перед записью UTF-8", pause)
    write_utf8(base / "note.txt", NOTE_TEXT)
    checkpoint("note.txt записан: можно открыть в редакторе", pause)
    inspect_encoding(base / "note.txt", NOTE_TEXT)
    checkpoint("Чтение и декодирование проверены", pause)
    extra = base / "extra.txt"
    write_utf8(extra, EXTRA_TEXT)
    data = extra.read_bytes()
    print("Дополнительный текст:\n" + EXTRA_TEXT)
    print("Символов:", len(EXTRA_TEXT))
    print("Байтов:", len(data))
    print("Кириллический символ в UTF-8 занимает больше одного байта.")
    checkpoint("Сравнение символов и байтов завершено", pause)
    return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Проверка кодировки текстового файла")
    parser.add_argument("--pause", action="store_true", help="ожидать Enter между фазами")
    main(pause=parser.parse_args().pause)
