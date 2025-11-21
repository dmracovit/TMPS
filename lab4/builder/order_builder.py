"""Order Builder - Builder Pattern from Lab 2"""
from models.order import Order
from models.menu_item import MenuItem


class OrderBuilder:
    """Builder for constructing complex orders"""
    
    def __init__(self, order_id: int):
        self._order = Order(order_id)
    
    def for_customer(self, customer_name: str) -> 'OrderBuilder':
        """Set customer name"""
        self._order.customer_name = customer_name
        return self
    
    def add_item(self, item: MenuItem) -> 'OrderBuilder':
        """Add item to order"""
        self._order.add_item(item)
        return self
    
    def with_special_instructions(self, instructions: str) -> 'OrderBuilder':
        """Add special instructions"""
        self._order.special_instructions = instructions
        return self
    
    def build(self) -> Order:
        """Build and return the order"""
        return self._order
