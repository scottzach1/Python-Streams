import functools
import warnings
from typing import Iterable, TypeVar, Iterator, List, Callable, Optional

T = TypeVar("T")


def _operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self: Stream = args[0]
        if not self.open:
            raise RuntimeError("The stream has been closed")
        return func(*args, **kwargs)

    return wrapper


def _terminal(func):
    @functools.wraps(func)
    @_operation
    def wrapper(*args, **kwargs):
        self: Stream = args[0]
        self.open = False
        return func(*args, **kwargs)

    return wrapper


class Stream:
    iterable: Iterator[T]
    open: bool

    def __init__(self, iterable: Iterable[T]):
        self.iterable = iter(iterable)
        self.open = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._verify_closed()

    def __del__(self):
        self._verify_closed()

    def _verify_closed(self):
        if self.open:
            warnings.warn("The stream was not closed", RuntimeWarning)
        self.open = False

    @_operation
    def apply(self, f: Callable[[T], T]) -> "Stream":
        self.iterable = (f(t) for t in self.iterable)
        return self

    @_operation
    def filter(self, f: Callable[[T], bool]) -> "Stream":
        self.iterable = (t for t in self.iterable if f(t))
        return self

    @_operation
    def reversed(self) -> "Stream":
        self.iterable = reversed(tuple(self.iterable))
        return self

    @_terminal
    def to_list(self) -> List[T]:
        return list(self.iterable)

    @_terminal
    def to_tuple(self):
        return tuple(self.iterable)

    @_terminal
    def to_iterable(self):
        return self.iterable

    @_terminal
    def to_set(self):
        return set(self.iterable)

    @_terminal
    def reduce(self, f: Callable[[T, T], T]) -> T:
        return functools.reduce(f, self.iterable)

    @_terminal
    def count(self):
        return sum(1 for _ in self.iterable)

    @_terminal
    def foreach(self, f: Callable[[T], None]) -> None:
        for t in self.iterable:
            f(t)

    @_terminal
    def find(self, f: Callable[[T], bool], default: T = None) -> Optional[T]:
        return next(filter(f, self.iterable), default)
