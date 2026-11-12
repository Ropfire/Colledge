"""Задания 1–6: безопасные операции в file_lab."""

import argparse
from pathlib import Path
from main import run_operations


def main(pause=False):
    print("Рабочая папка:", Path.cwd())
    return run_operations(Path.cwd() / "file_lab", "notes.txt", "notes_backup.txt",
                          "data.txt", "measurements.txt", pause=pause)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Учебные задания: файловые операции")
    parser.add_argument("--pause", action="store_true")
    main(pause=parser.parse_args().pause)
