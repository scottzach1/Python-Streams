import unittest

from python_streams import Stream


class TestOperation(unittest.TestCase):
    def test_apply(self):
        seed = [1, 2, 3]

        def double(n: int) -> int:
            return n * 2

        s = Stream(seed)
        s.apply(double)

        self.assertEqual(s.to_list(), [double(n) for n in seed])

    def test_filter(self):
        seed = range(100)

        def even(n: int) -> bool:
            return n % 2 == 0

        s = Stream(seed)
        s.filter(even)

        self.assertEqual(s.to_list(), list(range(0, 100, 2)))

    def test_reversed(self):
        seed = range(100)

        s = Stream(seed)
        s.reversed()

        self.assertEqual(s.to_list(), list(reversed(range(100))))
