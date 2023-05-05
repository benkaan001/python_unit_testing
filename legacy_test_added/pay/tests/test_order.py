from pay.order import Order, LineItem, OrderStatus

def test_empty_order_total() -> None:
    """Test that the total of an empty order is 0."""
    order = Order()
    assert order.total == 0

def test_order_total() -> None:
    """Test that the total of an order with a single line item is calculated correctly."""
    order = Order()
    order.line_items.append(LineItem(name="Coke", price=100))
    assert order.total == 100

def test_order_total_with_multiple_items() -> None:
    """Test that the total of an order with multiple line items is calculated correctly."""
    order = Order()
    order.line_items.append(LineItem(name="Coke", price=100))
    order.line_items.append(LineItem(name="Pepsi", price=100))
    assert order.total == 200

def test_order_pay() -> None:
    """Test that an order can be paid and its status is updated accordingly."""
    order = Order()
    order.pay()
    assert order.status == OrderStatus.PAID
