from pay.processor import PaymentProcessor
from dotenv import load_dotenv
import os
import pytest

# Load environment variables
load_dotenv()

# Set environment variables
CARD_NUMBER = os.getenv("CARD_NUMBER")
API_KEY = os.getenv("API_KEY")

"""
Tests for PaymentProcessor class.

Tests the following methods:
- PaymentProcessor.__init__
- PaymentProcessor.luhn_checksum
- PaymentProcessor.validate_card
- PaymentProcessor.charge
"""

def test_api_key_is_invalid() -> None:
    """
    Test that an error is raised when the provided API key is invalid.
    """
    processor = PaymentProcessor("invalid")
    with pytest.raises(ValueError):
        processor.charge(CARD_NUMBER, 12, 2024, 500)

def test_card_has_valid_date() -> None:
    """
    Test that a charge can be made with a card that has a valid expiration date.
    """
    processor = PaymentProcessor(API_KEY)
    processor.charge(CARD_NUMBER, 12, 2024, 500)

def test_card_has_invalid_date() -> None:
    """
    Test that an error is raised when a charge is attempted with a card that has an invalid expiration date.
    """
    processor = PaymentProcessor(API_KEY)
    with pytest.raises(ValueError):
        processor.charge(CARD_NUMBER, 12, 1900, 500)

def test_card_number_valid_luhn():
    """
    Test that the Luhn checksum method returns True when provided with a valid card number.
    """
    processor = PaymentProcessor(API_KEY)
    assert processor.luhn_checksum(CARD_NUMBER)

def test_card_number_invalid_luhn():
    """
    Test that an error is raised when a charge is attempted with a card that has an invalid expiration date.
    """
    processor = PaymentProcessor(API_KEY)
    assert not processor.luhn_checksum("1234")

def test_charge_card_valid():
    """
    Test that a charge can be made with a valid card.
    """
    processor = PaymentProcessor(API_KEY)
    processor.charge(CARD_NUMBER, 12, 2024, 500)

def test_charge_card_invalid():
    """
    Test that an error is raised when a charge is attempted with an invalid card.
    """
    processor = PaymentProcessor(API_KEY)
    with pytest.raises(ValueError):
        processor.charge("1234", 12, 2024, 500)