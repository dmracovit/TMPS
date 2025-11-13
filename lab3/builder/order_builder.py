from models.order import Order
from models.menu_item import MenuItem
from typing import List

class OrderBuilder:
    """Builder pattern for constructing orders"""
    
    def __init__(self, order_id: int):
        self._order = Order(order_id)
    
    def for_customer(self, customer_name: str):
        self._order.customer_name = customer_name
        return self
    
    def add_item(self, item: MenuItem):
        self._order.add_item(item)
        return self
    
    def add_items(self, items: List[MenuItem]):
        for item in items:
            self._order.add_item(item)
        return self
    
    def with_special_instructions(self, instructions: str):
        self._order.special_instructions = instructions
        return self
    
    def build(self) -> Order:
        if not self._order.items:
            raise ValueError("Order must contain at least one item")
        if not self._order.customer_name:
            raise ValueError("Order must have a customer name")
        return self._order
