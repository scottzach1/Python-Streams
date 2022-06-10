# Python-Streams

A pythonic (maybe) abstraction inspired by Java 8 streams

## Concepts

A Stream object acts a wrapper for an iterable object and provides a nice interface to provide a variety of "operations"
on. Once you have completed your operations, you can then collect the stream into a result using a "terminal".

- Operations mutate the `iterator` contained within the Stream object
- Terminals apply a closing operation to all operations on the `iterator`
- Once a terminal has been called you may **no longer** apply any operations.

## Usage

```python
from python_streams import Stream

"""
Basic Stream usage:
"""
seed = [1, 2, 3, 4]

with Stream(seed) as s:
    s.apply(lambda n: n * 10)
    s.apply(lambda n: n + 3)
    l = s.to_list()

assert l == [13, 23, 33, 43]

"""
You may also method chain operators
"""
seed = [1, 2, 3, 4]

with Stream(seed) as s:
    l = s.apply(lambda n: n * 10).apply(lambda n: n + 3).to_list()

assert l == [13, 23, 33, 43]
```
