from pay.order import Order
from typing import Protocol # replacing from pay.processor import PaymentProcessor
from pay.credit_card import CreditCard
from dotenv import load_dotenv
from pay.processor import CardExpiredError, InvalidMonthError


# instead of creating an instance of PaymentProcessor inside pay order define a protocol
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


def pay_order(order: Order, card: CreditCard, processor: PaymentProcessor) -> None:
    """Pay for an order using a given credit card and payment processor.

    This function initiates the payment process for the given order using the provided credit card
    and payment processor. If the payment is successful, the order is marked as paid.

    Args:
        order (Order): The order to be paid for.
        card (CreditCard): The credit card to be used for payment.
        processor (PaymentProcessor): The payment processor to be used for payment.

    Raises:
        ValueError: If the payment fails.

    Returns:
        None
    """
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
