from pay.processor import PaymentProcessor, luhn_checksum, CardExpiredError
from dotenv import load_dotenv
import os
import pytest
from datetime import date
from pay.credit_card import CreditCard

# Load environment variables
load_dotenv()

# Set environment variables
CARD_NUMBER = os.getenv("CARD_NUMBER")
API_KEY = os.getenv("API_KEY")


@pytest.fixture
def card() -> CreditCard:
    """
    Fixture that creates a CreditCard object with a card number and expiration date.

    The credit card returned by this fixture has a card number and expiration date that ensure
    it is always valid from two years from the current date.

    Returns:
        CreditCard: A CreditCard object with a valid card number and expiration date.
    """
    month = 12
    year = date.today().year + 2
    return CreditCard(CARD_NUMBER, month, year)


@pytest.fixture
def payment_processor() -> PaymentProcessor:
    """
    A fixture that returns an instance of PaymentProcessor class initialized with the API_KEY.

    Returns:
        PaymentProcessor: An instance of PaymentProcessor class.
    """
    return PaymentProcessor(API_KEY)



def test_api_key_is_invalid(card: CreditCard, payment_processor: PaymentProcessor) -> None:
    """
    Test that an error is raised when the provided API key is invalid.
    """
    with pytest.raises(ValueError):
        payment_processor = PaymentProcessor("invalid_api_key")
        payment_processor.charge(card, 500)


def test_card_has_valid_date(card: CreditCard, payment_processor: PaymentProcessor) -> None:
    """
    Test that a charge can be made with a card that has a valid expiration date.
    """
    payment_processor.charge(card, 500)


def test_card_has_invalid_date(card: CreditCard, payment_processor: PaymentProcessor) -> None:
    """
    Test that an error is raised when a charge is attempted with a card that has an invalid expiration date.
    """
    with pytest.raises(CardExpiredError):
        card.expiry_year = date.today().year - 1
        payment_processor.charge(card, 500)


def test_card_number_has_valid_luhn(card: CreditCard) -> None:
    """
    Test that a card number has a valid Luhn checksum.
    """
    assert luhn_checksum(card.number)


def test_card_number_has_invalid_luhn() -> None:
    """
    Test that a card number has an invalid Luhn checksum.
    """
    assert not luhn_checksum("1234")




def test_charge_card_valid(card: CreditCard, payment_processor: PaymentProcessor) -> None:
    """
    Test that a charge can be made with a valid card.
    """
    payment_processor.charge(card, 500)


def test_charge_card_invalid(card: CreditCard, payment_processor: PaymentProcessor) -> None:
    """
    Test that an error is raised when a charge is attempted with an invalid card.
    """
    with pytest.raises(ValueError):
        card.number = "1234"
        payment_processor.charge(card, 500)

