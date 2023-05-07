from datetime import datetime
from dotenv import load_dotenv
import os
from pay.credit_card import CreditCard

load_dotenv()

API_KEY = os.getenv("API_KEY")


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

# create a CardExpiredError class
class CardExpiredError(Exception):
    pass

class InvalidMonthError(Exception):
    pass



class PaymentProcessor:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _check_api_key(self) -> bool:
        return self.api_key == API_KEY


    def validate_card(self, card: CreditCard, month: int, year: int) -> bool:
        if not 1 <= month <= 12:
            raise InvalidMonthError("Invalid expiry month. Month must be in the range of 1 to 12.")
        expiry_date = datetime(year, month, 1)
        if expiry_date < datetime.now():
            raise CardExpiredError("Card is expired.")
        if not luhn_checksum(card.number):
            raise ValueError("Invalid Card number")
        return True

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