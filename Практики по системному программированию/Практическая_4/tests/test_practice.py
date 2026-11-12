import contextlib
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


class FileOperationTests(unittest.TestCase):
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

    def test_main_structure_and_repeat(self):
        base = main.main()
        expected = {"incoming/task.txt", "incoming/draft.txt", "incoming/memo_final.txt",
                    "backup/task_backup.txt", "ready/settings.txt"}
        snapshot = {str(p.relative_to(base)).replace("\\", "/"): p.read_bytes()
                    for p in base.rglob("*") if p.is_file()}
        self.assertEqual(set(snapshot), expected)
        self.assertEqual(snapshot["incoming/task.txt"], snapshot["backup/task_backup.txt"])
        for data in snapshot.values():
            self.assertGreaterEqual(len(data.decode("utf-8").splitlines()), 2)
        (base / "ready/settings.txt").write_text("Изменённые настройки", encoding="utf-8")
        (base / "backup/task_backup.txt").write_text("Неприкосновенная копия", encoding="utf-8")
        before = {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()}
        main.main()
        self.assertEqual(before, {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()})
        self.assertFalse((base / "incoming/config.txt").exists())
        self.assertFalse((base / "incoming/settings.txt").exists())
        self.assertFalse((base / "incoming/memo.txt").exists())

    def test_exercises_and_repeat(self):
        base = exercises.main()
        self.assertEqual({p.name for p in (base / "incoming").iterdir()}, {"notes.txt"})
        self.assertEqual((base / "incoming/notes.txt").read_bytes(), (base / "backup/notes_backup.txt").read_bytes())
        self.assertTrue((base / "ready/measurements.txt").is_file())
        exercises.main()
        self.assertFalse((base / "incoming/data.txt").exists())
        self.assertFalse((base / "incoming/measurements.txt").exists())

    def test_operations_preserve_targets(self):
        for operation in (main.safe_copy, main.safe_rename, main.safe_move):
            with self.subTest(operation=operation.__name__):
                source = Path("source.txt")
                target = Path("target.txt")
                source.write_bytes(b"source")
                target.write_bytes(b"target must stay")
                self.assertFalse(operation(source, target))
                self.assertEqual(target.read_bytes(), b"target must stay")
                self.assertEqual(source.read_bytes(), b"source")

    def test_missing_sources_and_directory_sources(self):
        Path("folder").mkdir()
        for operation in (main.safe_copy, main.safe_rename, main.safe_move):
            self.assertFalse(operation(Path("missing.txt"), Path("result.txt")))
            self.assertFalse(operation(Path("folder"), Path("result.txt")))
            self.assertFalse(Path("result.txt").exists())

    def test_missing_target_parent(self):
        Path("source.txt").write_bytes(b"original")
        for operation in (main.safe_copy, main.safe_rename, main.safe_move):
            self.assertFalse(operation(Path("source.txt"), Path("absent/result.txt")))
            self.assertEqual(Path("source.txt").read_bytes(), b"original")

    def test_initial_creation_never_overwrites_or_recreates(self):
        source = Path("source.txt")
        source.write_bytes(b"keep")
        self.assertFalse(main.create_source(source, "новый текст"))
        self.assertEqual(source.read_bytes(), b"keep")
        Path("final.txt").write_bytes(b"keep final")
        self.assertFalse(main.create_source(Path("missing.txt"), "новый текст", (Path("final.txt"),)))
        self.assertFalse(Path("missing.txt").exists())

    def test_target_directory_is_conflict(self):
        Path("source.txt").write_bytes(b"keep")
        Path("target").mkdir()
        for operation in (main.safe_copy, main.safe_rename, main.safe_move):
            self.assertFalse(operation(Path("source.txt"), Path("target")))
        self.assertEqual(list(Path("target").iterdir()), [])

    def test_pause_phases(self):
        with patch("builtins.input", return_value="") as wait:
            main.main(pause=True)
        self.assertEqual(wait.call_count, 6)


if __name__ == "__main__":
    unittest.main()
