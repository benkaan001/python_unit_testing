from pay.order import LineItem, Order
from pay.payment import CreditCard,pay_order
from pay.processor import PaymentProcessor, API_KEY



def main():
    # Test card number: 1249190007575069
    card_number = input('Please enter your card number: ')
    month = int(input('Please enter the card expiration month: '))
    year = int(input('Please enter the card expiration year: '))
    card = CreditCard(card_number, month, year)
    processor = PaymentProcessor(API_KEY)
    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    order.line_items.append(LineItem(name="Hat", price=50_00))
    pay_order(order, card, processor)

if __name__ == '__main__':
    main()
