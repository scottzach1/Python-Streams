#! /bin/python3
#                 _   _                 _     _
#   ___  ___ ___ | |_| |_ ______ _  ___| |__ / |
#  / __|/ __/ _ \| __| __|_  / _` |/ __| '_ \| |
#  \__ \ (_| (_) | |_| |_ / / (_| | (__| | | | |
#  |___/\___\___/ \__|\__/___\__,_|\___|_| |_|_|
#
#       Zac Scott (github.com/scottzach1)
#
# https://github.com/scottzach1/python-streams

import functools
import warnings
from typing import Iterable, TypeVar, Iterator, List, Callable, Optional, Tuple, Set

T = TypeVar("T")
V = TypeVar("V")


def _operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self: Stream = args[0]
        self._verify_open()
        return func(*args, **kwargs)

    return wrapper


def _terminal(func):
    @functools.wraps(func)
    @_operation
    def wrapper(*args, **kwargs):
        self: Stream = args[0]
        self.close()
        return func(*args, **kwargs)

    return wrapper


class Stream:
    __iterable: Iterator[T]
    __open: bool

    def __init__(self, iterable: Iterable[T]):
        self.__iterable = iter(iterable)
        self.__open = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._verify_closed()
        self.close()

    def __del__(self):
        self._verify_closed()
        self.close()

    def _verify_closed(self):
        if self.__open:
            warnings.warn("The stream was not closed", RuntimeWarning)

    def _verify_open(self):
        if not self.open:
            raise RuntimeError("The stream has been closed")

    @property
    def open(self):
        return self.__open

    def close(self):
        self.__open = False

    @_operation
    def apply(self, f: Callable[[T], V]) -> "Stream":
        self.__iterable = (f(t) for t in self.__iterable)
        return self

    @_operation
    def filter(self, f: Callable[[T], bool]) -> "Stream":
        self.__iterable = (t for t in self.__iterable if f(t))
        return self

    @_operation
    def reversed(self) -> "Stream":
        self.__iterable = reversed(tuple(self.__iterable))
        return self

    @_terminal
    def to_list(self) -> List[T]:
        return list(self.__iterable)

    @_terminal
    def to_tuple(self) -> Tuple:
        return tuple(self.__iterable)

    @_terminal
    def to_iterable(self) -> Iterable[T]:
        return self.__iterable

    @_terminal
    def to_set(self) -> Set[T]:
        return set(self.__iterable)

    @_terminal
    def collect(self, f: Callable[[T], V]) -> V:
        return f(self.__iterable)

    @_terminal
    def reduce(self, f: Callable[[T, T], T]) -> T:
        return functools.reduce(f, self.__iterable)

    @_terminal
    def count(self) -> int:
        return sum(1 for _ in self.__iterable)

    @_terminal
    def empty(self) -> bool:
        try:
            next(self.__iterable)
            return False
        except StopIteration:
            return True

    @_terminal
    def foreach(self, f: Callable[[T], None]) -> None:
        for t in self.__iterable:
            f(t)

    @_terminal
    def find(self, f: Callable[[T], bool], default: T = None) -> Optional[T]:
        return next(filter(f, self.__iterable), default)

    @_terminal
    def first(self):
        return next(self.__iterable)

    def last(self):
        return self.reduce(lambda _l, r: r)
