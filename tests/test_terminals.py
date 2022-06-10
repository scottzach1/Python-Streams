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

    def test_reduce(self):
        seed = ["a", "b", "c"]
        s = Stream(seed)

        self.assertEqual(s.reduce(str.__add__), "abc")

    def test_count(self):
        seed = range(100)
        s = Stream(seed)

        self.assertEqual(s.count(), 100)
