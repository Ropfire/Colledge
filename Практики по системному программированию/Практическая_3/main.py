"""Практическая №3. Анализатор рабочей папки. Зыков Е. Т., ИСиП-23-1."""

import argparse
from pathlib import Path


def checkpoint(message, pause=False):
    print("\n=== " + message + " ===", flush=True)
    if pause:
        input("Enter — продолжить: ")


def create_structure(base, folders):
    for name in folders:
        (base / name).mkdir(parents=True, exist_ok=True)
    files = {
        "materials/theory.txt": "Каталог содержит файлы и подпапки.\nPath помогает работать с путями.\n",
        "reports/result.txt": "Структура создана средствами Python.\nРезультат проверен через iterdir().\n",
        "logs/session.log": "Учебная программа запущена.\n",
    }
    for name, text in files.items():
        path = base / name
        if not path.exists():
            with open(path, "x", encoding="utf-8", newline="\n") as file:
                file.write(text)


def show_folder(folder):
    print("\nСодержимое:", folder)
    file_count = 0
    folder_count = 0
    if not folder.is_dir():
        print("Каталог не найден")
        return file_count, folder_count
    for item in sorted(folder.iterdir()):
        if item.is_file():
            print("[ФАЙЛ]", item.name)
            file_count += 1
        elif item.is_dir():
            print("[КАТАЛОГ]", item.name)
            folder_count += 1
    print("Файлов:", file_count, "Каталогов:", folder_count)
    return file_count, folder_count


def analyze(base):
    print("Полный путь:", base)
    print("Существует:", base.exists())
    print("Это каталог:", base.is_dir())
    print("Это файл:", base.is_file())
    show_folder(base)
    materials = show_folder(base / "materials")[0]
    reports = show_folder(base / "reports")[0]
    print(f"Итог: в materials файлов — {materials}; в reports — {reports}.")


def main(pause=False):
    print("Рабочая папка:", Path.cwd())
    base = Path.cwd() / "workspace"
    checkpoint("Перед созданием workspace", pause)
    create_structure(base, ("materials", "reports", "logs", "temp"))
    analyze(base)
    checkpoint("Основная структура создана и проверена", pause)
    notes = base / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    readme = notes / "readme.txt"
    if not readme.exists():
        with open(readme, "x", encoding="utf-8", newline="\n") as file:
            file.write("Заметки Зыкова Егора о работе с каталогами.\n")
    show_folder(base)
    show_folder(notes)
    checkpoint("Дополнение notes/readme.txt проверено", pause)
    return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Анализатор рабочей папки")
    parser.add_argument("--pause", action="store_true", help="ожидать Enter между фазами")
    main(pause=parser.parse_args().pause)
