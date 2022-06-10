# Python-Streams

A pythonic (maybe) abstraction inspired by Java 8 streams

## Concepts

A Stream object acts a wrapper for an iterable object and provides a nice interface to provide a variety of "operations"
on. Once you have completed your operations, you can then collect the stream into a result using a "terminal".

- Operations mutate the `iterator` contained within the Stream object
- Terminals apply a closing operation to all operations on the `iterator`
- Once a terminal has been called you may **no longer** apply any operations.

### Operations

| Operation  | Description                                                    |
|:-----------|:---------------------------------------------------------------|
| apply()    | Apply a function to each element (acts as a map function).     |
| filter()   | Filter the elements with a filter function.                    |
| reversed() | Reverse the elements in the stream (must consume full stream). |

### Terminals

| Terminal      | Description                                                 |
|:--------------|:------------------------------------------------------------|
| to_list()     | Collects the elements into a list.                          |
| to_tuple()    | Collects the elements into a tuple.                         |
| to_iterable() | Collects the elements into an iterable.                     |
| to_set()      | Collects the elements into a set.                           |
| collect()     | Collects the elements by applying function to the iterable. |
| reduce()      | Reduces the elements to a single value using a function.    |
| count()       | Counts the number of items in the stream.                   |
| empty()       | Checks whether the stream is empty.                         |
| foreach()     | Applies a function for each element bu returns nothing.     |
| find()        | Finds the first item in stream matching a filter function.  |
| first()       | Finds the first item in the stream.                         |
| last()        | Finds the last item in the stream.                          |

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
