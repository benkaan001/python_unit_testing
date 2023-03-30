# **PYTHON UNIT TESTING**

This is a collection of examples about unit testing in Python. Unit testing is an essetial component of agile development.

The motivation behind this repository is to explore key concepts and keep it as a resource for future reference.


# Writing Tests with Pytest

The first step is to install Pytest using `pip`:

```
pip install pytest
```
Pytest looks for test functions that start with the prefix `test_`.

# Example class: MyList

Let's begin by defining a custom class called MyList. This class is a basic implementation of a list with some of its `special methods` marked with double underscore - `"dunder"`- overridden.


```python
import pytest

class MyList:
    def __init__(self, *args):
        self.data = list(args)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def __contains__(self, value):
        return value in self.data

my_list = MyList(1, 2, 3, 4, 5)

if __name__ == '__main__':
    pytest.main(['test_dunder.py']) # will run the tests defined in `test_dunder.py` module

```

The MyList class has six methods implemented:

- `__init__`: initializes the list with any number of values passed as arguments.
- `__len__`: returns the length of the list.
- `__getitem__`: returns the value at the given index.
- `__setitem__`: sets the value at the given index.
- `__delitem__`: removes the item at the given index.
- `__contains__`: returns whether a given value is in the list.

The variable `my_list` is an instance of the MyList class.

Here are some tests for the MyList class.


```python
import pytest
from script import MyList


def test_constructor():
    lst = MyList(1, 2, 3)
    assert len(lst) == 3
    assert lst[0] == 1
    assert lst[1] == 2
    assert lst[2] ==

def test_len():
    lst = MyList(1, 2, 3)
    assert len(lst) == 3

def test_getitem():
    lst = MyList(1, 2, 3)
    assert lst[0] == 1
    assert lst[1] == 2
    assert lst[2] == 3
    with pytest.raises(IndexError):
        item = lst[3]

def test_setitem():
    lst = MyList(1, 2, 3)
    lst[1] = 4
    assert lst[1] == 4

def test_delitem():
    lst = MyList(1, 2, 3)
    del lst[1]
    assert len(lst) == 2
    assert lst[0] == 1
    assert lst[1] == 3
    with pytest.raises(IndexError):
        item = lst[2]

def test_contains():
    lst = MyList(1, 2, 3)
    assert 2 in lst
    assert 4 not in lst
```
Here are the steps to elevate this testing to the next level.

