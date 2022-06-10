import unittest

from python_streams.steams import Stream


class TestStream(unittest.TestCase):

    def test_to_list(self):
        seed = ["a", "b"]

        s = Stream(seed)

        self.assertEqual(seed, s.to_list())

    def test_stream_closed(self):
        seed = ["a", "b"]

        s = Stream(seed)
        s.to_list()
        with self.assertRaises(RuntimeError):
            s.to_list()

    def test_stream_closed_context_manager(self):
        seed = ["a", "b"]

        with Stream(seed) as stream:
            stream.apply(lambda c: c)

        with self.assertRaises(RuntimeError):
            stream.apply(lambda c: c)

    def test_apply(self):
        seed = [1, 2, 3]

        def double(n: int) -> int:
            return n * 2

        s = Stream(seed)
        s.apply(double)

        self.assertEqual(s.to_list(), [double(n) for n in seed])
