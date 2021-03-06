import contextlib
import unittest

from python_streams import Stream


class TestStream(unittest.TestCase):
    def test_stream_context_closes(self):
        seed = ["a", "b"]

        with contextlib.suppress(RuntimeWarning):
            with Stream(seed) as s:
                self.assertTrue(s.open)

        self.assertFalse(s.open)

    def test_stream_terminal_closes(self):
        seed = ["a", "b"]

        s = Stream(seed)
        self.assertTrue(s.open)
        s.to_list()
        self.assertFalse(s.open)

    def test_stream_closed_error(self):
        seed = ["a", "b"]

        s = Stream(seed)
        s.to_list()
        with self.assertRaises(RuntimeError):
            s.to_list()

    def test_stream_context_close_warning(self):
        seed = ["a", "b"]

        with self.assertWarns(RuntimeWarning):
            with Stream(seed) as _s:
                pass

    def test_stream_scope_close_warning(self):
        def helper():
            seed = ["a", "b"]
            _s = Stream(seed)

        with self.assertWarns(RuntimeWarning):
            helper()

    def test_stream_closed_context_manager(self):
        seed = ["a", "b"]

        with Stream(seed) as stream:
            stream.apply(lambda c: c)

        with self.assertRaises(RuntimeError):
            stream.apply(lambda c: c)

    def test_method_chaining(self):
        seed = [1, 2, 3]

        def double(n: int) -> int:
            return n * 2

        with Stream(seed) as s1:
            s1.apply(double)
            s1.apply(double)
            res1 = s1.to_list()

        with Stream(seed) as s2:
            res2 = s2.apply(double).apply(double).to_list()

        self.assertEqual(res1, res2)
