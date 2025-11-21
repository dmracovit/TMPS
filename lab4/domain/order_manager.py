"""Order Manager - Singleton Pattern from Lab 2"""
from models.order import Order
from typing import List, Optional


class OrderManager:
    """Singleton class for managing all orders"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._orders: List[Order] = []
        self._next_order_id = 1
        self._initialized = True
    
    def create_order(self, customer_name: str = "") -> Order:
        """Create a new order"""
        order = Order(self._next_order_id, customer_name)
        self._orders.append(order)
        self._next_order_id += 1
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get order by ID"""
        for order in self._orders:
            if order.order_id == order_id:
                return order
        return None
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return self._orders.copy()
    
    def complete_order(self, order_id: int) -> bool:
        """Mark order as completed"""
        order = self.get_order(order_id)
        if order:
            order.set_status("delivered")
            return True
        return False
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order"""
        order = self.get_order(order_id)
        if order:
            order.set_status("cancelled")
            return True
        return False
    
    def get_total_revenue(self) -> float:
        """Calculate total revenue from completed orders"""
        return sum(order.total for order in self._orders if order.status == "delivered")
