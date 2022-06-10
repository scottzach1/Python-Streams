import contextlib
import io
import unittest
from typing import Iterable

from python_streams import Stream


class TestTerminal(unittest.TestCase):
    def test_to_list(self):
        seed = ("a", "b")
        s = Stream(seed)

        self.assertEqual(list(seed), s.to_list())

    def test_to_tuple(self):
        seed = ["a", "b"]
        s = Stream(seed)

        self.assertEqual(tuple(seed), s.to_tuple())

    def test_to_iterable(self):
        seed = ["a", "b"]
        s = Stream(seed)
        iterable = s.to_iterable()

        self.assertIsInstance(iterable, Iterable)
        self.assertEqual(list(iterable), seed)

    def test_to_set(self):
        seed = ["a", "b", "b"]
        s = Stream(seed)

        self.assertEqual(set(seed), s.to_set())

    def test_collect(self):
        seed = ["a", "b", "c"]
        collectors = [list, tuple, set]

        for collector in collectors:
            self.assertEqual(collector(seed), Stream(seed).collect(collector))

    def test_reduce(self):
        seed = ["a", "b", "c"]
        s = Stream(seed)

        self.assertEqual(s.reduce(str.__add__), "abc")

    def test_count(self):
        seed = range(100)
        s = Stream(seed)

        self.assertEqual(s.count(), 100)

    def test_empty_true(self):
        seed = []
        s = Stream(seed)

        self.assertTrue(s.empty())

    def test_empty_false(self):
        seed = ["a", "b", "c"]
        s = Stream(seed)

        self.assertFalse(s.empty())

    def test_foreach(self):
        seed = ["a", "b", "c"]
        s = Stream(seed)

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            s.foreach(lambda n: print(f"_{n}", end=""))

        self.assertEqual(f.getvalue(), "".join((f"_{s}" for s in seed)))

    def test_find(self):
        seed = ["aerosmith", "beatles", "car"]
        s = Stream(seed)

        def find(text: str) -> bool:
            return text.startswith("b")

        self.assertEqual(s.find(find), "beatles")

    def test_first(self):
        seed = ["a", "b", "c"]
        s = Stream(seed)

        self.assertEqual(s.first(), "a")

    def test_first_raises(self):
        seed = []
        s = Stream(seed)

        with self.assertRaises(StopIteration):
            s.first()

    def test_last(self):
        seed = ["a", "b", "c"]
        s = Stream(seed)

        self.assertEqual(s.last(), "c")

    def test_last_raises(self):
        seed = []
        s = Stream(seed)

        with self.assertRaises(TypeError):
            print(s.last())
