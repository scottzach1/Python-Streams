from typing import Iterable, TypeVar, Iterator, List

T = TypeVar("T")


class Stream:
    iterable: Iterator[T]

    def __init__(self, iterable: Iterable[T]):
        self.iterable = iter(iterable)

    def to_list(self) -> List[T]:
        return list(self.iterable)
