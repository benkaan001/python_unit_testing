from dataclasses import dataclass, field
from enum import Enum

class OrderStatus(Enum):
    OPEN = 'open'
    PAID = 'paid'

@dataclass
class LineItem:
    name: str
    price: str
    quantity: int = 1

    @property
    def total(self) -> int:
        """ Returns the total cost of the line item (price * quantity)."""
        return self.price * self.quantity

@dataclass
class Order:
    line_items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN

    @property
    def total(self) -> int:
        """ Returns the total cost of the order (sum of all line items)."""
        return sum(item.total for item in self.line_items)

    def pay(self) -> None:
        """ Changes the status of the order to PAID."""
        self.status = OrderStatus.PAID
