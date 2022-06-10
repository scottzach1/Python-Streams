import unittest

from python_streams.steams import Stream


class TestStream(unittest.TestCase):

    def test_to_list(self):
        seed = ["a", "b"]

        s = Stream(seed)

        self.assertEqual(seed, s.to_list())
