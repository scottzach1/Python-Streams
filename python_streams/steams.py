from typing import Iterable, TypeVar, Iterator, List, Callable

T = TypeVar("T")


class Stream:
    iterable: Iterator[T]

    def __init__(self, iterable: Iterable[T]):
        self.iterable = iter(iterable)

    def to_list(self) -> List[T]:
        return list(self.iterable)

    def apply(self, f: Callable[[T], T]):
        self.iterable = (f(t) for t in self.iterable)
