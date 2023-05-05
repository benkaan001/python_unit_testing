from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

class PaymentProcessor:
    def __init__(self, api_key: str) -> None:
        self.api_key = API_KEY

    def _check_api_key(self) -> bool:
        return self.api_key == API_KEY

    def luhn_checksum(self, card_number: str) -> bool:
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

    def validate_card(self, card: str, month: int, year: int) -> bool:
        return self.luhn_checksum(card) and datetime(year, month, 1) > datetime.now()

    def charge(self, card: str, month: int, year: int, amount: int) -> None:
        if not self.validate_card(card, month, year):
            raise ValueError("Invalid Card")
        if not self._check_api_key():
            raise ValueError("Invalid API key")
        print(f"Charging card number {card} for ${amount/100:.2f}")