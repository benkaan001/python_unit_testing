## Unit Testing For Legacy Code

This project involved refactoring legacy code that had no testing. Unit testing was added to the codebase, using `pytest` testing library. The purpose of this project was to demonstrate how unit testing can help write better code.

Unit testing can help identify bugs and ensure that changes made to the code do not break existing functionality.

In this project, unit testing also led to the modularization of the code, making it more maintainable.

## Testing

The test coverage report showed that the refactored code has a 97% test coverage. This gives confidence that the code is working as expected.

```
===================================================== test session starts =====================================================

---------- coverage: platform darwin, python 3.11.2-final-0 ----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
pay/__init__.py                   0      0   100%
pay/credit_card.py                6      0   100%
pay/order.py                     22      0   100%
pay/payment.py                   23      3    87%
pay/processor.py                 45      1    98%
pay/tests/__init__.py             0      0   100%
pay/tests/test_line_item.py      20      0   100%
pay/tests/test_order.py          17      0   100%
pay/tests/test_payment.py        45      3    93%
pay/tests/test_processor.py      37      0   100%
-------------------------------------------------
TOTAL                           215      7    97%


===================================================== 20 passed in 0.05s ======================================================
```

In order to test ***pay_oder*** functionality, `MonkeyPatch` object from pytest was initially used to ***mock*** the user inputs to run unit tests.

```py
def test_pay_order(monkeypatch: MonkeyPatch) -> None:

    # 3. Define a mock version of the charge method to avoid 'charging' the card during testing.
    def mock_charge(self: PaymentProcessor, card: str, month: int, year: int, amount: int) -> None:
        pass

    # Define the inputs to be used by the test.
    inputs = ["1249190007575069", "12", "2024"]

    # 1. Mock the input function to simulate user input by returning the next input in the inputs list.
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    # 2. Mock the check_api_key method to always return True, since we don't want to test it here.
    monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)

    # 4. Mock the charge method of PaymentProcessor to use the mock_charge method defined above.
    monkeypatch.setattr(PaymentProcessor, "charge", mock_charge)

    # Create an Order object with a single line item.
    order = Order()
    order.line_items.append(LineItem(name="Coke", price=300))

    # Call pay_order with the mocked user input and PaymentProcessor charge method.
    pay_order(order)

    # Check if order status is updated to PAID after payment
    assert order.status == OrderStatus.PAID
```


Though ***patching*** initially helped test the code, as it became harder to write unit testing code, refactoring became inevitable.


## Refactor Changes


The refactored version introduced the following changes:

1. ***Use of a protocol:*** Instead of using a concrete class `PaymentProcessor`, the refactored code defines a protocol that abstracts away the implementation details. This makes the code more flexible and easier to test, as it is now possible to use different payment processors that conform to the same interface.

```py
class PaymentProcessor(Protocol):
    """A protocol defining the interface for payment processors.

    PaymentProcessor defines the required methods for any payment processor implementation.
    Any class implementing this protocol must provide the following methods:

    - validate_card(card: CreditCard, month: int, year: int) -> bool
    - charge(card: CreditCard, amount: int, month: int, year: int) -> bool
    """
    def validate_card(self, card: CreditCard, month: int, year: int) -> None:
        """Validates the card with the given expiry date"""
        pass
    def charge(self, card: str, amount: float) -> None:
        """Charges the card with the amount"""
        pass
```



2. ***Use of `CreditCard` class:*** The refactored code replaces the raw string input for the card details with a `CreditCard` class. This makes it easier to handle and validate card details as a single object.

```py
@dataclass
class CreditCard:
    number: str
    expiry_month: str
    expiry_year: str
```

3. ***Separation of concerns:*** The refactored code separates the payment process into two distinct parts: validating the card and charging the card. This makes it easier to handle and communicate specific errors that may occur during the payment process.

```py
    def validate_card(self, card: CreditCard, month: int, year: int) -> bool:
        if not 1 <= month <= 12:
            raise InvalidMonthError("Invalid expiry month. Month must be in the range of 1 to 12.")
        expiry_date = datetime(year, month, 1)
        if expiry_date < datetime.now():
            raise CardExpiredError("Card is expired.")
        if not luhn_checksum(card.number):
            raise ValueError("Invalid Card number")
        return True
```

```py
   def charge(self, card: CreditCard, amount: int) -> None:
        try:
            self.validate_card(card, card.expiry_month, card.expiry_year)
        except CardExpiredError:
            raise CardExpiredError("Card validation failed: Card is expired.")
        except ValueError as e:
            raise ValueError(f"Card validation failed: {e}")
        if not self._check_api_key():
            raise ValueError("Invalid API key")
        print(f"Charging card number {card} for ${amount/100:.2f}")
```
Removed the ***luhn_checksum()*** call from the `validate_card()` method, as it is now called outside the class. Moved the `luhn_checksum()` function outside the `PaymentProcessor` class, making it a separate function that can be accessed from anywhere in the module.

```py
def luhn_checksum(card_number: str) -> bool:
        def digits_of(card_nr: str):
            return [int(d) for d in card_nr]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum =0
        checksum += sum(odd_digits)
        for digit in even_digits:
            checksum += sum(digits_of(str(digit * 2)))
        return checksum % 10 == 0
```


4. ***Better error handling:*** The refactored code improves on the error handling by using specific exceptions (`CardExpiredError` and `InvalidMonthError`) instead of the general `ValueError` used in the original code. This makes it easier to handle specific errors and provide better feedback to the user.

```py
class CardExpiredError(Exception):
    pass

class InvalidMonthError(Exception):
    pass

def pay_order(order: Order, card: CreditCard, processor: PaymentProcessor) -> None:
    amount = order.total
    if amount == 0:
        raise ValueError("Cannot pay an order with total 0.")

    try:
        processor.validate_card(card, card.expiry_month, card.expiry_year)
        processor.charge(card, amount)
    except CardExpiredError:
        print("Card is expired. Please use a different card.")
    except InvalidMonthError:
        print("Invalid expiry month. Please enter a valid month between 1 and 12.")
    except ValueError as e:
        print(f"Payment failed: {e}")
    else:
        order.pay()
        print(f"Order paid in full: ${order.total/100:.2f}")
```

### ***Error Handling***

1. Created custom exception classes to handle specific errors that may occur in the payment process, such as ***CardExpiredError*** and ***InvalidMonthError***. This allows us to raise more informative errors that can be caught and handled appropriately.

2. Modified the ***pay_order*** function to catch these custom exceptions and print user-friendly error messages instead of raising generic ***ValueError*** exceptions.

3. Added input validation to the ***CreditCard*** class to ensure that the card number, expiry month, and expiry year are valid before attempting to use them in the payment process.

Overall, the changes made the code more modular and easier to maintain, by separating the functions that can be used elsewhere in the module, and defining custom exception classes to handle specific exceptions during card validation.



