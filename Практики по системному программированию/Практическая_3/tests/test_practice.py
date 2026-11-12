import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main
import exercises


class DirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.temp.name)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()

    def tearDown(self):
        self.output.__exit__(None, None, None)
        os.chdir(self.previous)
        self.temp.cleanup()

    def test_exercises_structure_and_counts(self):
        base = exercises.main()
        self.assertEqual(base, Path.cwd() / "practice40")
        self.assertEqual(main.show_folder(base), (0, 3))
        for name in ("materials/theory.txt", "reports/result.txt"):
            self.assertGreaterEqual(len((base / name).read_text(encoding="utf-8").splitlines()), 2)
        self.assertEqual(main.show_folder(base / "materials"), (1, 0))
        self.assertEqual(main.show_folder(base / "reports"), (1, 0))
        self.assertTrue((base / "logs/session.log").is_file())

    def test_main_and_repeat_preserve_existing_files(self):
        base = main.main()
        self.assertEqual(main.show_folder(base), (0, 5))
        self.assertEqual(main.show_folder(base / "notes"), (1, 0))
        file = base / "materials/theory.txt"
        file.write_text("Собственное содержимое", encoding="utf-8")
        before = {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()}
        main.main()
        self.assertEqual(before, {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()})
        self.assertTrue((base / "temp").is_dir())

    def test_missing_folder_and_pause(self):
        self.assertEqual(main.show_folder(Path("missing")), (0, 0))
        with patch("builtins.input", return_value="") as wait:
            main.main(pause=True)
        self.assertEqual(wait.call_count, 3)


if __name__ == "__main__":
    unittest.main()
