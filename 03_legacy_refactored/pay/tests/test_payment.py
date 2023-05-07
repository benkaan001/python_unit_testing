from pay.order import Order, LineItem, OrderStatus
from pay.payment import pay_order
import pytest
from pay.credit_card import CreditCard
from datetime import date
from pay.payment import InvalidMonthError, CardExpiredError, PaymentProcessor


@pytest.fixture
def card() -> CreditCard:
    # Make sure the card is always valid from 2 years from current date
    year = date.today().year + 2
    month = 12
    return CreditCard("1249190007575069", month, year)


class PaymentProcessorMock(PaymentProcessor):

    def charge(self, card: CreditCard, amount: int) -> None:
        pass

    def validate_card(self, card: CreditCard, month: int, year: int) -> None:
        # Raise an InvalidMonthError if the month is greater than 12
        if not 1 <= month <= 12:
            raise InvalidMonthError("Invalid expiry month. Month must be in the range of 1 to 12.")

        # Raise a CardExpiredError if the card has already expired
        if date.today() > date(year, month, 1):
            raise CardExpiredError("Card has expired")


def test_pay_order_valid(card: CreditCard) -> None:
    # Create an Order object with a single line item.
    order = Order()
    order.line_items.append(LineItem(name="Coke", price=300))

    # Call pay_order with the mocked user input and the mocked PaymentProcessor class.
    pay_order(order, card, PaymentProcessorMock())

    # Check if order status is updated to PAID after payment
    assert order.status == OrderStatus.PAID


def test_pay_order_invalid(card: CreditCard) -> None:
    with pytest.raises(ValueError):
        order = Order()
        pay_order(order, card, PaymentProcessorMock())
        assert order.status == OrderStatus.PAID

def test_pay_order_invalid_card_month(card: CreditCard) -> None:
    card.expiry_month = 15
    with pytest.raises(InvalidMonthError):
        order = Order()
        order.line_items.append(LineItem(name="Coke", price=300))
        pay_order(order, card, PaymentProcessorMock())
        PaymentProcessorMock().validate_card(card, card.expiry_month, card.expiry_year)
        # Check if order status is not updated to PAID after payment due to invalid month
        assert order.status == OrderStatus.OPEN

def test_pay_order_card_expired(card: CreditCard) -> None:
    card.expiry_year = date.today().year - 1
    with pytest.raises(CardExpiredError):
        order = Order()
        order.line_items.append(LineItem(name="Coke", price=300))
        pay_order(order, card, PaymentProcessorMock())
        PaymentProcessorMock().validate_card(card, card.expiry_month, card.expiry_year)
        assert order.status == OrderStatus.OPEN
