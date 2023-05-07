from pay.order import LineItem

def test_line_item_total() -> None:
    """Test that the total price of a LineItem is calculated correctly."""
    line_item = LineItem(name='Test', price=1000)
    assert line_item.total == 1000

def test_line_item_quantity() -> None:
    """Test that the total price of a LineItem is calculated
    correctly when the quantity is greater than 1."""
    line_item = LineItem(name='Test', price=1000, quantity=5)
    assert line_item.total == 5000

# add additional tests for the LineItem class here

def test_line_item_init() -> None:
    """Test that a LineItem can be initialized with the correct values."""
    line_item = LineItem(name='Test', price=1000, quantity=5)
    assert line_item.name == 'Test'
    assert line_item.price == 1000
    assert line_item.quantity == 5

def test_line_item_name() -> None:
    """Test that the name property of a LineItem can be set and retrieved."""
    line_item = LineItem(name='Test', price=1000)
    line_item.name = 'New Test'
    assert line_item.name == 'New Test'

def test_line_item_price() -> None:
    """Test that the price property of a LineItem can be set and retrieved."""
    line_item = LineItem(name='Test', price=1000)
    line_item.price = 2000
    assert line_item.price == 2000