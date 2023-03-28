from pay.order import Lineitem, Order
from pay.payment import pay_order

def main():
    # Test card number: 1249190007575069
    order = Order()
    order.line_items.append(Lineitem(name="Shoes", price=100_00, quantity=2))
    order.line_items.append(Lineitem(name="Hat", price=50_00))
    pay_order(order)

if __name__ == '__main__':
    main()