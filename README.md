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

# 1.Use descriptive test names:
Use descriptive names for each test case that clearly state what the test is doing. For example, instead of `test_constructor`, use `test_mylist_constructor_with_valid_values`.

# 2.Use pytest fixtures:
Pytest fixtures can help reduce code duplication and make tests more readable. For example, instead of creating a new MyList object in each test, create a fixture that returns a MyList object.



```python
class TestMyList:
    @pytest.fixture
    def mylist(self):
        return MyList(1, 2, 3)

    def test_mylist_constructor_with_valid_values(self, mylist):
        assert len(mylist) == 3
        assert mylist[0] == 1
        assert mylist[1] == 2
        assert mylist[2] == 3

    def test_mylist_len(self, mylist):
        assert len(mylist) == 3

    def test_mylist_getitem_with_valid_index(self, mylist):
        assert mylist[0] == 1
        assert mylist[1] == 2
        assert mylist[2] == 3

    def test_mylist_getitem_with_invalid_index(self, mylist):
        with pytest.raises(IndexError):
            item = mylist[3]

    def test_mylist_setitem(self, mylist):
        mylist[1] = 4
        assert mylist[1] == 4

    def test_mylist_delitem(self, mylist):
        del mylist[1]
        assert len(mylist) == 2
        assert mylist[0] == 1
        assert mylist[1] == 3
        with pytest.raises(IndexError):
            item = mylist[2]

    def test_mylist_contains_with_existing_value(self, mylist):
        assert 2 in mylist

    def test_mylist_contains_with_non_existing_value(self, mylist):
        assert 4 not in mylist
```
# 3.Use assert statements with custom error messages:
When an assert statement fails, it can be hard to understand what went wrong. You can provide custom error messages to make it easier to understand what the problem is.


```python

class TestMyList:
    @pytest.fixture
    def mylist(self):
        return MyList(1, 2, 3)

    def test_mylist_constructor_with_valid_values(self, mylist):
        assert len(mylist) == 3, "MyList should have a length of 3"
        assert mylist[0] == 1, "First element should be 1"
        assert mylist[1] == 2, "Second element should be 2"
        assert mylist[2] == 3, "Third element should be 3"

    def test_mylist_len(self, mylist):
        assert len(mylist) == 3, "MyList should have a length of 3"

    def test_mylist_getitem_with_valid_index(self, mylist):
        assert mylist[0] == 1, "First element should be 1"
        assert mylist[1] == 2, "Second element should be 2"
        assert mylist[2] == 3, "Third element should be 3"

    def test_mylist_getitem_with_invalid_index(self, mylist):
        with pytest.raises(IndexError):
            item = mylist[3]

    def test_mylist_setitem(self, mylist):
        mylist[1] = 4
        assert mylist[1] == 4, "Second element should be 4 after setting it"

    def test_mylist_delitem(self, mylist):
        del mylist[1]
        assert len(mylist) == 2, "MyList should have a length of 2 after deleting an element"
        assert mylist[0] == 1, "First element should be 1 after deleting the second element"
        assert mylist[1] == 3, "Second element should be 3 after deleting the second element"
        with pytest.raises(IndexError):
            item = mylist[2]

    def test_mylist_contains_with_existing_value(self, mylist):
        assert 2 in mylist, "2 should be in MyList"

    def test_mylist_contains_with_non_existing_value(self, mylist):
        assert 4 not in mylist, "4 should not be in MyList"```

```
In this implementation, each assert statement has a custom error message that describes what should have happened in case of a failure. This makes it easier to understand what went wrong and how to fix the problem.

# 4.Use parametrized fixtures:
Using parametrized fixtures makes tests more concise, readable, and maintainable by eliminating repetitive code and allowing to test multiple inputs with a single fixture. It also makes it easier to add new test cases in the future, ensuring that tests remain comprehensive and up-to-date.


```python
class TestMyList:
    @pytest.fixture(params=[(1, 2, 3), (4, 5, 6, 7, 8), (9,)])
    def mylist(self, request):
        return MyList(*request.param)

    def test_mylist_constructor_with_valid_values(self, mylist):
        assert len(mylist) == len(request.param), "MyList should have the correct length"
        for i, value in enumerate(request.param):
            assert mylist[i] == value, f"MyList[{i}] should be {value}"

    def test_mylist_len(self, mylist):
        assert len(mylist) == len(request.param), "MyList should have the correct length"

    def test_mylist_getitem_with_valid_index(self, mylist):
        for i, value in enumerate(request.param):
            assert mylist[i] == value, f"MyList[{i}] should be {value}"

    def test_mylist_getitem_with_invalid_index(self, mylist):
        with pytest.raises(IndexError):
            item = mylist[len(request.param)]

    def test_mylist_setitem(self, mylist):
        mylist[1] = 4
        assert mylist[1] == 4, "Second element should be 4 after setting it"

    def test_mylist_delitem(self, mylist):
        del mylist[1]
        assert len(mylist) == len(request.param) - 1, \
        "MyList should have the correct length after deleting an element"
        for i, value in enumerate(request.param):
            if i < 1:
                assert mylist[i] == value, \
                f"MyList[{i}] should be {value} after deleting the second element"
            else:
                assert mylist[i - 1] == value, \
                f"MyList[{i - 1}] should be {value} after deleting the second element"
        with pytest.raises(IndexError):
            item = mylist[len(request.param) - 1]

    def test_mylist_contains_with_existing_value(self, mylist):
        assert request.param[1] in mylist, \
        f"{request.param[1]} should be in MyList"

    def test_mylist_contains_with_non_existing_value(self, mylist):
        assert not (request.param[1] + 1) in mylist, \
        f"{request.param[1] + 1} should not be in MyList"```
```

In this implementation, the `mylist` fixture is now parametrized with different lists of values, so each test function will run multiple times with a different set of values. The `request.param` object is used to access the current set of values being tested.

The test functions have been modified to handle the different sets of values, using the `request.param` object to access the correct values for each scenario. For example, in the `test_mylist_constructor_with_valid_values` function, the expected length and values are now obtained from `request.param`, instead of being hardcoded.

This way, the tests are more concise and less repetitive, while still covering multiple scenarios.


## 5.Add docstrings:
It's always good practice to add docstrings to your tests so that others can understand what the tests are supposed to do.

```python
class TestMyList:
    @pytest.fixture(params=[(1, 2, 3), (4, 5, 6, 7, 8), (9,)])
    def mylist(self, request):
        return MyList(*request.param)

    def test_mylist_constructor_with_valid_values(self, mylist):
        """
        Test that the MyList constructor creates a list with the expected elements.

        The test checks that the length of the created list matches the length of the input values,
        and that each element of the list matches the corresponding input value.
        """
        assert len(mylist) == len(request.param), "MyList should have the correct length"
        for i, value in enumerate(request.param):
            assert mylist[i] == value, f"MyList[{i}] should be {value}"

    def test_mylist_len(self, mylist):
        """
        Test that the __len__ method of MyList returns the correct length of the list.
        """
        assert len(mylist) == len(request.param), "MyList should have the correct length"

    def test_mylist_getitem_with_valid_index(self, mylist):
        """
        Test that the __getitem__ method of MyList returns the correct element for a valid index.
        """
        for i, value in enumerate(request.param):
            assert mylist[i] == value, f"MyList[{i}] should be {value}"

    def test_mylist_getitem_with_invalid_index(self, mylist):
        """
        Test that the __getitem__ method of MyList raises an IndexError for an invalid index.
        """
        with pytest.raises(IndexError):
            item = mylist[len(request.param)]

    def test_mylist_setitem(self, mylist):
        """
        Test that the __setitem__ method of MyList sets the correct value for a valid index.
        """
        mylist[1] = 4
        assert mylist[1] == 4, "Second element should be 4 after setting it"

    def test_mylist_delitem(self, mylist):
        """
        Test that the __delitem__ method of MyList deletes the correct element
        and updates the length and indexes of the list.
        """
        del mylist[1]
        assert len(mylist) == len(request.param) - 1, \
        "MyList should have the correct length after deleting an element"
        for i, value in enumerate(request.param):
            if i < 1:
                assert mylist[i] == value, \
                f"MyList[{i}] should be {value} after deleting the second element"
            else:
                assert mylist[i - 1] == value, \
                f"MyList[{i - 1}] should be {value} after deleting the second element"
        with pytest.raises(IndexError):
            item = mylist[len(request.param) - 1]

    def test_mylist_contains_with_existing_value(self, mylist):
        """
        Test that the __contains__ method of MyList returns True for an existing value.
        """
        assert request.param[1] in mylist, f"{request.param[1]} should be in MyList"

    def test_mylist_contains_with_non_existing_value(self, mylist):
        """
        Test that the __contains__ method of MyList returns False for a non-existing value.
        """
        assert not (request.param[1] + 1) in mylist, \
        f"{request.param[1] + 1} should not be in MyList"
```
# Conclusion
Despite the numerous benefits of writing great tests, it is not always feasible to achieve. One of the biggest challenges is that writing comprehensive tests can be time-consuming, especially for complex systems that require a lot of `edge case` testing. In addition, maintaining and updating tests can be challenging as systems change and evolve over time. Another challenge is ensuring that tests remain relevant and effective as new features are added to the system.

Furthermore, testing requires a deep understanding of the system being tested, as well as knowledge of best practices and testing tools. This can be a significant learning curve for developers who may be more focused on implementing new features rather than testing them. Additionally, there may be trade-offs between the cost of writing and maintaining tests versus the potential benefits of identifying and preventing bugs.

Despite these challenges, the benefits of writing great tests, such as reduced risk of bugs, improved maintainability, and increased confidence in code changes, make it a worthwhile investment.