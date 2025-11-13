from typing import Dict, List, Optional
from models.order import Order

class OrderManager:
    """Singleton pattern - manages all orders"""
    _instance: Optional['OrderManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not OrderManager._initialized:
            self.orders: Dict[int, Order] = {}
            self.next_order_id = 1
            OrderManager._initialized = True
    
    def create_order(self) -> Order:
        order = Order(self.next_order_id)
        self.orders[self.next_order_id] = order
        self.next_order_id += 1
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> List[Order]:
        return list(self.orders.values())
    
    def get_pending_orders(self) -> List[Order]:
        return [order for order in self.orders.values() if order.status == "pending"]
    
    def complete_order(self, order_id: int):
        if order_id in self.orders:
            self.orders[order_id].status = "completed"
    
    def cancel_order(self, order_id: int):
        if order_id in self.orders:
            self.orders[order_id].status = "cancelled"
    
    def get_total_revenue(self) -> float:
        return sum(order.get_total() for order in self.orders.values() if order.status == "completed")
