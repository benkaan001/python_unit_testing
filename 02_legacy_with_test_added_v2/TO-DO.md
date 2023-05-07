## Apply `separation of concerns` principle

When working with legacy code or test-driven development, it's often beneficial to apply the `separation of concerns` principle. This principle helps to isolate different responsibilities of a program into distinct modules or functions, making the code easier to test and maintain.

In the following example, we have a legacy `pay_order()` function that has a complex structure. It requires several layers of user input as well as creating a `PaymentProcessor` object.


```py
def pay_order(order: Order):
    if order.total == 0:
        raise ValueError("Cannot pay an order with total 0.")
    card = input('Please enter your card number: ')
    month = int(input('Please enter the card expiration month: '))
    year = int(input('Please enter the card expiration year: '))
    payment_processor = PaymentProcessor(API_KEY)
    payment_processor.charge(card, month, year, amount=order.total)
    order.pay()
```

In order to run unit tests on the `pay_oder()` logic - ***test_payment.py***, we can either refactor the code, or use the `MonkeyPatch` object from pytest to `mock` the user inputs to run unit tests.

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

In its current form, it's difficult to test ***pay_order()*** because it has many dependencies, including user input and the `PaymentProcessor` object.

Though `patching` helps test the code, things can get complicated quickly. That is why, we need to consider refactoring the legacy code.




