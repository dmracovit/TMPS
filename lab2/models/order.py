from datetime import datetime
from typing import List
from models.menu_item import MenuItem

class Order:
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.items: List[MenuItem] = []
        self.timestamp = datetime.now()
        self.status = "pending"
        self.customer_name = ""
        self.special_instructions = ""
    
    def add_item(self, item: MenuItem):
        self.items.append(item)
    
    def remove_item(self, item: MenuItem):
        if item in self.items:
            self.items.remove(item)
    
    def get_total(self) -> float:
        return sum(item.price for item in self.items)
    
    def __str__(self):
        items_str = ", ".join([item.name for item in self.items])
        return f"Order #{self.order_id} for {self.customer_name}: {items_str} - Total: ${self.get_total():.2f}"
    
    def __repr__(self):
        return f"Order(id={self.order_id}, items={len(self.items)}, total=${self.get_total():.2f})"
