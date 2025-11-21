"""Order model with observer support"""
from typing import List, Optional
from datetime import datetime
from .menu_item import MenuItem

class Order:
    """Order class representing a customer order with observer pattern support"""
    
    def __init__(self, order_id: int, customer_name: str = ""):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items: List[MenuItem] = []
        self.status = "pending"
        self.special_instructions = ""
        self.created_at = datetime.now()
        self.total = 0.0
        self._observers = []  # For Observer pattern
    
    def add_item(self, item: MenuItem):
        """Add item to order"""
        self.items.append(item)
        self.calculate_total()
    
    def remove_item(self, item: MenuItem):
        """Remove item from order"""
        if item in self.items:
            self.items.remove(item)
            self.calculate_total()
    
    def calculate_total(self):
        """Calculate order total"""
        self.total = sum(item.get_price() for item in self.items)
    
    def set_status(self, status: str):
        """Set order status and notify observers"""
        old_status = self.status
        self.status = status
        self.notify_observers(old_status, status)
    
    # Observer Pattern methods
    def attach(self, observer):
        """Attach an observer to the order"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Detach an observer from the order"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, old_status: str, new_status: str):
        """Notify all observers about status change"""
        for observer in self._observers:
            observer.update(self, old_status, new_status)
    
    def __str__(self):
        items_str = "\n  ".join([str(item) for item in self.items])
        return (f"Order #{self.order_id} - {self.customer_name}\n"
                f"Status: {self.status}\n"
                f"Items:\n  {items_str}\n"
                f"Total: ${self.total:.2f}")
