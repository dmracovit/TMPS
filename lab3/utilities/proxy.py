from datetime import datetime
from typing import List, Optional
from models.order import Order
from domain.order_manager import OrderManager

class OrderManagerProxy:
    """
    PROXY PATTERN
    Provides a proxy for OrderManager with additional functionality:
    - Logging all operations
    - Caching frequently accessed orders
    - Access control (future enhancement)
    """
    
    def __init__(self):
        self._real_manager = OrderManager()
        self._cache = {}
        self._access_log = []
    
    def _log_access(self, operation: str, details: str = ""):
        """Log all operations"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {operation}: {details}"
        self._access_log.append(log_entry)
        print(f"🔍 LOG: {log_entry}")
    
    def create_order(self) -> Order:
        """Create order with logging"""
        self._log_access("CREATE_ORDER", "New order created")
        order = self._real_manager.create_order()
        self._cache[order.order_id] = order
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get order with caching"""
        # Check cache first
        if order_id in self._cache:
            self._log_access("GET_ORDER", f"Order #{order_id} retrieved from cache")
            return self._cache[order_id]
        
        # If not in cache, get from real manager
        self._log_access("GET_ORDER", f"Order #{order_id} retrieved from storage")
        order = self._real_manager.get_order(order_id)
        if order:
            self._cache[order_id] = order
        return order
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders with logging"""
        self._log_access("GET_ALL_ORDERS", f"Total orders: {len(self._real_manager.orders)}")
        return self._real_manager.get_all_orders()
    
    def complete_order(self, order_id: int):
        """Complete order with cache invalidation"""
        self._log_access("COMPLETE_ORDER", f"Order #{order_id} marked as completed")
        self._real_manager.complete_order(order_id)
        # Invalidate cache
        if order_id in self._cache:
            del self._cache[order_id]
    
    def cancel_order(self, order_id: int):
        """Cancel order with cache invalidation"""
        self._log_access("CANCEL_ORDER", f"Order #{order_id} cancelled")
        self._real_manager.cancel_order(order_id)
        # Invalidate cache
        if order_id in self._cache:
            del self._cache[order_id]
    
    def get_total_revenue(self) -> float:
        """Get revenue with logging"""
        revenue = self._real_manager.get_total_revenue()
        self._log_access("GET_REVENUE", f"Total revenue: ${revenue:.2f}")
        return revenue
    
    def get_access_log(self) -> List[str]:
        """Get the access log"""
        return self._access_log.copy()
    
    def clear_cache(self):
        """Clear the cache"""
        self._log_access("CLEAR_CACHE", f"Cleared {len(self._cache)} cached orders")
        self._cache.clear()
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        return {
            "cached_orders": len(self._cache),
            "total_operations": len(self._access_log)
        }
