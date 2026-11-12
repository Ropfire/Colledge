"""Практическая №4. Организатор тестовых файлов. Зыков Е. Т., ИСиП-23-1."""

import argparse
from pathlib import Path
from shutil import copy2, move


def checkpoint(message, pause=False):
    print("\n=== " + message + " ===", flush=True)
    if pause:
        input("Enter — продолжить: ")


def create_source(path, text, later_paths=()):
    """Не воссоздаёт исходник, если цепочка уже дошла до следующего имени."""
    if path.exists() or path.is_symlink():
        print("Существующий путь сохранён:", path)
        return False
    for later in later_paths:
        if later.exists() or later.is_symlink():
            print("Исходник не воссоздан: следующий путь уже занят:", later)
            return False
    if not path.parent.is_dir():
        print("Родительский каталог отсутствует:", path.parent)
        return False
    try:
        with open(path, "x", encoding="utf-8", newline="\n") as file:
            file.write(text)
    except OSError as error:
        print("Ошибка создания:", error)
        return False
    print("Создан:", path)
    return True


def safe_operation(source, target, operation):
    if not source.exists() or not source.is_file() or source.is_symlink():
        print("Исходный файл не найден или не является обычным файлом:", source)
        return False
    if target.exists() or target.is_symlink():
        print("Целевой путь уже существует, операция пропущена:", target)
        return False
    if not target.parent.is_dir():
        print("Целевой каталог отсутствует:", target.parent)
        return False
    try:
        if operation == "copy":
            copy2(source, target)
        elif operation == "rename":
            source.rename(target)
        elif operation == "move":
            move(str(source), str(target))
        else:
            raise ValueError("Неизвестная операция: " + operation)
    except OSError as error:
        print("Операция не выполнена:", error)
        return False
    print(f"{operation}: {source} -> {target}")
    print("Исходный путь существует:", source.exists())
    print("Целевой путь существует:", target.exists())
    if operation == "copy":
        success = source.is_file() and target.is_file() and source.read_bytes() == target.read_bytes()
    else:
        success = not source.exists() and target.is_file()
    print("Проверка результата:", success)
    return success


def safe_copy(source, target):
    return safe_operation(source, target, "copy")


def safe_rename(source, target):
    return safe_operation(source, target, "rename")


def safe_move(source, target):
    return safe_operation(source, target, "move")


def show_folder(folder):
    print("\nСодержимое:", folder)
    if not folder.is_dir():
        print("Каталог не найден")
        return
    for item in sorted(folder.iterdir()):
        if item.is_file():
            print("[ФАЙЛ]", item.name)
        elif item.is_dir():
            print("[КАТАЛОГ]", item.name)


def prepare(base, source_name, copy_name, rename_name, final_name, extra=False):
    for name in ("incoming", "backup", "ready"):
        (base / name).mkdir(parents=True, exist_ok=True)
    incoming = base / "incoming"
    create_source(incoming / source_name, "Учебная задача Зыкова Егора.\nСтатус: подготовлена к копированию.\n",
                  (base / "backup" / copy_name,))
    create_source(incoming / rename_name, "Параметры учебной программы.\nРежим: безопасные операции.\n",
                  (incoming / final_name, base / "ready" / final_name))
    if extra:
        create_source(incoming / "draft.txt", "Черновик отчёта.\nПроверить результаты операций.\n")
        create_source(incoming / "memo.txt", "Памятка по работе.\nНе перезаписывать целевые файлы.\n",
                      (incoming / "memo_final.txt",))
    return incoming


def run_operations(base, source_name, copy_name, rename_name, final_name, pause=False, extra=False):
    incoming = prepare(base, source_name, copy_name, rename_name, final_name, extra)
    for name in ("incoming", "backup", "ready"):
        show_folder(base / name)
    checkpoint("Исходная структура: перед копированием", pause)
    safe_copy(incoming / source_name, base / "backup" / copy_name)
    checkpoint("После копирования: перед переименованием", pause)
    safe_rename(incoming / rename_name, incoming / final_name)
    checkpoint("После переименования: перед перемещением", pause)
    safe_move(incoming / final_name, base / "ready" / final_name)
    checkpoint("После перемещения", pause)
    if extra:
        safe_rename(incoming / "memo.txt", incoming / "memo_final.txt")
        checkpoint("Самостоятельное переименование memo завершено", pause)
    for name in ("incoming", "backup", "ready"):
        show_folder(base / name)
    checkpoint("Итоговая структура проверена", pause)
    return base


def main(pause=False):
    print("Рабочая папка:", Path.cwd())
    return run_operations(Path.cwd() / "workspace_ops", "task.txt", "task_backup.txt",
                          "config.txt", "settings.txt", pause=pause, extra=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Организатор тестовых файлов")
    parser.add_argument("--pause", action="store_true", help="ожидать Enter между операциями")
    main(pause=parser.parse_args().pause)
