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
