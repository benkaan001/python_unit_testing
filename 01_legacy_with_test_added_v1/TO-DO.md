## Add tests

Adding unit tests to legacy code requires a structured approach.Here are some general steps you can follow to add unit tests to legacy code:

1. `Identify the critical areas of the legacy code`: Identify the most critical areas of the codebase that have the highest risk of breaking, such as complex business logic, frequently modified modules, and the modules that have the most dependencies.

2. `Start small`: Begin with writing unit tests for the smallest and simplest parts of the codebase. Once you have a solid foundation, you can build on it by writing tests for larger and more complex areas.
- `Order` and `LineItem` will be a good start

3. `Use the right testing framework`: Choose a testing framework that is appropriate for your codebase, programming language, and the size of your team. There are several testing frameworks available, such as JUnit, pytest, and Jasmine.

4. `Mock dependencies`: In legacy code, dependencies are often tightly coupled, making it difficult to write unit tests. To overcome this issue, you can use mocking frameworks to simulate the behavior of dependencies.

5. `Refactor the code`: Refactoring the code will make it easier to test. This will involve identifying and removing code smells, reducing the size of the methods, and separating the code into smaller, more manageable pieces.

6. `Automate the tests`: To ensure that the tests are run regularly and consistently, you should automate them. This can be done using a Continuous Integration (CI) tool, which will run the tests automatically whenever changes are made to the codebase.

7. `Review and update the tests`:` As the codebase evolves, it's important to update the tests accordingly. This will ensure that the tests remain relevant and effective.

In summary, adding unit tests to legacy code requires careful planning and execution. Start small, use the right testing framework, mock dependencies, refactor the code, automate the tests, and review and update the tests regularly.

### Test Coverage After `test_line_item.py`

```
pytest --cov

---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                                                                                 Stmts   Miss  Cover
--------------------------------------------------------------------------------------------------------
/Users/benkaan/Library/Python/3.11/lib/python/site-packages/anyio/pytest_plugin.py      96     88     8%
__init__.py                                                                              0      0   100%
pay/__init__.py                                                                          0      0   100%
pay/order.py                                                                            22      2    91%
pay/tests/__init__.py                                                                    0      0   100%
pay/tests/test_line_item.py                                                              7      0   100%
--------------------------------------------------------------------------------------------------------
TOTAL                                                                                  125     90    28%

```

### Test Coverage After `test_order.py`
```
---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                                                                                 Stmts   Miss  Cover
--------------------------------------------------------------------------------------------------------
/Users/benkaan/Library/Python/3.11/lib/python/site-packages/anyio/pytest_plugin.py      96     88     8%
__init__.py                                                                              0      0   100%
pay/__init__.py                                                                          0      0   100%
pay/order.py                                                                            22      0   100%
pay/tests/__init__.py                                                                    0      0   100%
pay/tests/test_line_item.py                                                              7      0   100%
pay/tests/test_order.py                                                                 17      0   100%
--------------------------------------------------------------------------------------------------------
TOTAL                                                                                  142     88    38%
```



### Getting the html report

Run:
- `coverage html` or `python3 -m coverage html` - to run it as module instead of a package
- open the index.html with LiveServer
![coverage_report](htmlcov/html_cov_report.png)




