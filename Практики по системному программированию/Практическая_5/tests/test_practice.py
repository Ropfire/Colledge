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


class EncodingTests(unittest.TestCase):
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

    def assert_utf8_lf(self, path, text):
        self.assertEqual(path.read_bytes(), text.encode("utf-8"))
        self.assertNotIn(b"\r", path.read_bytes())
        self.assertEqual(main.read_utf8(path), text)

    def test_main_text_bytes_and_counts(self):
        base = main.main()
        self.assertEqual(base, Path.cwd() / "encoding_check")
        self.assertGreaterEqual(len(main.NOTE_TEXT.splitlines()), 3)
        self.assert_utf8_lf(base / "note.txt", main.NOTE_TEXT)
        self.assert_utf8_lf(base / "extra.txt", main.EXTRA_TEXT)
        self.assertGreater(len((base / "extra.txt").read_bytes()), len(main.EXTRA_TEXT))
        result = main.inspect_encoding(base / "note.txt", main.NOTE_TEXT)
        self.assertTrue(result["matches"])
        self.assertEqual(result["utf8"], main.NOTE_TEXT)
        self.assertNotEqual(result["latin1"], main.NOTE_TEXT)
        self.assertEqual(result["data"][:20], main.NOTE_TEXT.encode("utf-8")[:20])

    def test_exercises(self):
        base = exercises.main()
        self.assert_utf8_lf(base / "texts/student.txt", exercises.STUDENT_TEXT)
        self.assert_utf8_lf(base / "texts/profile.txt", exercises.PROFILE_TEXT)
        self.assertGreaterEqual(len(exercises.STUDENT_TEXT.splitlines()), 2)
        self.assertGreaterEqual(len(exercises.PROFILE_TEXT.splitlines()), 3)
        self.assertIn("Зыков Егор Тимурович", exercises.PROFILE_TEXT)
        self.assertIn("ИСиП-23-1", exercises.PROFILE_TEXT)

    def test_repeat_has_identical_bytes(self):
        for program in (main.main, exercises.main):
            base = program()
            before = {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()}
            program()
            self.assertEqual(before, {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()})

    def test_inspect_detects_different_expected_text(self):
        file = Path("text.txt")
        main.write_utf8(file, "Русский текст\n")
        self.assertFalse(main.inspect_encoding(file, "Другой текст")["matches"])

    def test_pause_phases(self):
        with patch("builtins.input", return_value="") as wait:
            main.main(pause=True)
        self.assertEqual(wait.call_count, 4)


if __name__ == "__main__":
    unittest.main()
