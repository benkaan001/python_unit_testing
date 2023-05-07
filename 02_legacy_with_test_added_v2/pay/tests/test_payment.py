from pay.order import Order, LineItem, OrderStatus
from pay.payment import pay_order
from pay.processor import PaymentProcessor

# import MonkeyPatch
from pytest import MonkeyPatch
import pytest


def test_pay_order_valid(monkeypatch: MonkeyPatch) -> None:
    """
    Test the pay_order function by mocking user input and PaymentProcessor charge method.

    Uses MonkeyPatch to mock user input and PaymentProcessor charge method
    and ensure that pay_order correctly calls PaymentProcessor.charge method.

    Args:
        monkeypatch: Instance of MonkeyPatch pytest fixture for mocking.

    Returns:
        None
    """
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


def test_pay_order_invalid(monkeypatch: MonkeyPatch) -> None:
    with pytest.raises(ValueError):
        def mock_charge(self: PaymentProcessor, card: str, month: int, year: int, amount: int) -> None:
            pass
        inputs = ["0000000000000000", "12", "2024"]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
        monkeypatch.setattr(PaymentProcessor, "charge", mock_charge)
        order=Order()
        # pass an empty order that should raise ValueError
        pay_order(order)
        assert order.status == OrderStatus.PAID
