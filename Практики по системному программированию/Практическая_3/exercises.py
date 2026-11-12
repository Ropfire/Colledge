"""Задания 1–8: создание и исследование practice40."""

import argparse
from pathlib import Path
from main import analyze, checkpoint, create_structure


def main(pause=False):
    print("Рабочая папка:", Path.cwd())
    base = Path.cwd() / "practice40"
    checkpoint("Перед созданием practice40", pause)
    create_structure(base, ("materials", "reports", "logs"))
    checkpoint("Каталоги и тестовые файлы созданы", pause)
    analyze(base)
    checkpoint("Классификация и подсчёты завершены", pause)
    return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Учебные задания: каталоги")
    parser.add_argument("--pause", action="store_true")
    main(pause=parser.parse_args().pause)
