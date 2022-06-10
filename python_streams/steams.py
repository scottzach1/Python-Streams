import functools
from typing import Iterable, TypeVar, Iterator, List, Callable

T = TypeVar("T")


def _open(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self: Stream = args[0]
        if not self.open:
            raise RuntimeError("The stream has been closed")
        return func(*args, **kwargs)

    return wrapper


class Stream:
    iterable: Iterator[T]
    open: bool

    def __init__(self, iterable: Iterable[T]):
        self.iterable = iter(iterable)
        self.open = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open = False

    @_open
    def to_list(self) -> List[T]:
        self.open = False
        return list(self.iterable)

    @_open
    def apply(self, f: Callable[[T], T]) -> "Stream":
        self.iterable = (f(t) for t in self.iterable)
        return self
