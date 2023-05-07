from pay.order import Order
from pay.processor import PaymentProcessor

def pay_order(order: Order):
    if order.total == 0:
        raise ValueError("Cannot pay an order with total 0.")
    card = input('Please enter your card number: ')
    month = int(input('Please enter the card expiration month: '))
    year = int(input('Please enter the card expiration year: '))
    payment_processor = PaymentProcessor('0super-1secret-2api-3key')
    payment_processor.charge(card, month, year, amount=order.total)
    order.pay()