from pay.order import LineItem

def test_line_item_total() -> None:
    line_item = LineItem(name='Test', price=1000)
    assert line_item.total == 1000

def test_line_item_quantity() -> None:
    line_item = LineItem(name='Test', price=1000, quantity=5)
    assert line_item.total == 5000
