from models.order import Order
from models.menu_item import MenuItem
from typing import List

class OrderBuilder:
    """
    BUILDER PATTERN
    Provides a fluent interface for constructing complex Order objects step by step.
    Allows building orders with various configurations and validations.
    """
    
    def __init__(self, order_id: int):
        self._order = Order(order_id)
    
    def for_customer(self, customer_name: str):
        """Set customer name"""
        self._order.customer_name = customer_name
        return self
    
    def add_item(self, item: MenuItem):
        """Add a single menu item"""
        self._order.add_item(item)
        return self
    
    def add_items(self, items: List[MenuItem]):
        """Add multiple menu items"""
        for item in items:
            self._order.add_item(item)
        return self
    
    def with_special_instructions(self, instructions: str):
        """Add special instructions to the order"""
        self._order.special_instructions = instructions
        return self
    
    def set_status(self, status: str):
        """Set order status"""
        self._order.status = status
        return self
    
    def build(self) -> Order:
        """Build and return the final Order object"""
        if not self._order.items:
            raise ValueError("Order must contain at least one item")
        if not self._order.customer_name:
            raise ValueError("Order must have a customer name")
        return self._order
    
    def reset(self):
        """Reset the builder to create a new order"""
        self._order = Order(self._order.order_id)
        return self


class ComboMealBuilder(OrderBuilder):
    """
    Specialized builder for creating combo meals
    Extends OrderBuilder with combo-specific functionality
    """
    
    def __init__(self, order_id: int):
        super().__init__(order_id)
    
    def add_combo(self, main_course: MenuItem, side: MenuItem, beverage: MenuItem):
        """Add a complete combo meal (main + side + beverage)"""
        self._order.add_item(main_course)
        self._order.add_item(side)
        self._order.add_item(beverage)
        return self
    
    def add_family_combo(self, main_courses: List[MenuItem], sides: List[MenuItem], 
                         beverages: List[MenuItem], dessert: MenuItem = None):
        """Add a family-sized combo meal"""
        for item in main_courses:
            self._order.add_item(item)
        for item in sides:
            self._order.add_item(item)
        for item in beverages:
            self._order.add_item(item)
        if dessert:
            self._order.add_item(dessert)
        return self


class OrderDirector:
    """
    Director class that knows how to build specific types of orders
    using the OrderBuilder
    """
    
    def __init__(self):
        self.builder: OrderBuilder = None
    
    def set_builder(self, builder: OrderBuilder):
        """Set the builder to use"""
        self.builder = builder
    
    def build_quick_lunch(self, customer_name: str, main: MenuItem, beverage: MenuItem) -> Order:
        """Build a quick lunch order"""
        return (self.builder
                .for_customer(customer_name)
                .add_item(main)
                .add_item(beverage)
                .with_special_instructions("Quick lunch - please rush")
                .build())
    
    def build_dinner_combo(self, customer_name: str, main: MenuItem, side: MenuItem, 
                          beverage: MenuItem, dessert: MenuItem) -> Order:
        """Build a complete dinner combo"""
        return (self.builder
                .for_customer(customer_name)
                .add_item(main)
                .add_item(side)
                .add_item(beverage)
                .add_item(dessert)
                .with_special_instructions("Complete dinner combo")
                .build())
