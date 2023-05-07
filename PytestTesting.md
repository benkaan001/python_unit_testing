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
    assert lst[2] == 3

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
# List of Potential Improvements

### 1. Organize the test cases into a class to improve readability and maintainability.

### 2. Using a fixture create a MyList object that can be reused across multiple tests, which in turn will reduce code duplication.

### 3. Use parametrization to test multiple input/output scenarios for the MyList constructor, rather than repeating the same test code multiple times.

### 4. Add custom error messages to provide information about what went wrong if the assertion fails.

### 5. Add docstrings to describe what each test case is testing to improving readability.

```python

import pytest
from topics.dunder.script import MyList


class TestMyList:
    """
    A test suite for the MyList class.
    """

    @pytest.fixture
    def my_list(self):
        """
        Fixture that returns an instance of MyList with some initial values.
        """
        return MyList(1, 2, 3)

    @pytest.mark.parametrize("input_list, expected_list", [
        ([1, 2, 3], [1, 2, 3]),
        ([4, 5, 6], [4, 5, 6]),
        (["a", "b", "c"], ["a", "b", "c"])
    ])
    def test_constructor(self, input_list, expected_list):
        """
        Test the constructor of the MyList class with various input values.
        """
        my_list = MyList(*input_list)
        assert len(my_list) == len(expected_list), \
            f"Expected length of {len(expected_list)}, but got {len(my_list)}"
        for i in range(len(expected_list)):
            assert my_list[i] == expected_list[i], \
                f"Expected {expected_list[i]}, but got {my_list[i]}"

    def test_len(self, my_list):
        """
        Test the __len__ method of the MyList class.
        """
        assert len(my_list) == 3, f"Expected length of 3, but got {len(my_list)}"

    @pytest.mark.parametrize("index, expected_value", [
        (0, 1),
        (1, 2),
        (2, 3)
    ])
    def test_getitem_with_valid_index(self, my_list, index, expected_value):
        """
        Test the __getitem__ method of the MyList class with valid indices.
        """
        assert my_list[index] == expected_value, \
            f"Expected {expected_value}, but got {my_list[index]}"

    def test_getitem_with_invalid_index(self, my_list):
        """
        Test the __getitem__ method of the MyList class with an invalid index.
        """
        with pytest.raises(IndexError, match="list index out of range"):
            item = my_list[3]

    def test_setitem(self, my_list):
        """
        Test the __setitem__ method of the MyList class.
        """
        my_list[1] = 4
        assert my_list[1] == 4, f"Expected 4, but got {my_list[1]}"

    def test_delitem(self, my_list):
        """
        Test the __delitem__ method of the MyList class.
        """
        del my_list[1]
        assert len(my_list) == 2, f"Expected length of 2, but got {len(my_list)}"
        assert my_list[0] == 1, f"Expected 1, but got {my_list[0]}"
        assert my_list[1] == 3, f"Expected 3, but got {my_list[1]}"
        with pytest.raises(IndexError, match="list index out of range"):
            item = my_list[2]

    def test_contains_with_existing_value(self, my_list):
        """
        Test the __contains__ method of the MyList class
        with a value that exists in the list.
        """
        assert 2 in my_list, "Expected value not found in list"

    def test_contains_with_non_existing_value(self, my_list):
        """
        Test the __contains__ method of the MyList class
        with a value that does not exist in the list.
        """
        assert 4 not in my_list, \
            f"Expected value 4 to not be in the list, but it was found"

```