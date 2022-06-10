import functools
import warnings
from typing import Iterable, TypeVar, Iterator, List, Callable

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
        if self.open:
            warnings.warn("The stream was not closed", RuntimeWarning)
        self.open = False

    @_terminal
    def to_list(self) -> List[T]:
        return list(self.iterable)

    @_operation
    def apply(self, f: Callable[[T], T]) -> "Stream":
        self.iterable = (f(t) for t in self.iterable)
        return self
