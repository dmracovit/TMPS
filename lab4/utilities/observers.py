"""
Observer Pattern - Order Status Notification System

This module implements observers that react to order status changes.
Multiple observers can monitor orders and take different actions.
"""
from abc import ABC, abstractmethod
from models.order import Order
from datetime import datetime


class OrderObserver(ABC):
    """Abstract base class for order observers"""
    
    @abstractmethod
    def update(self, order: Order, old_status: str, new_status: str):
        """Called when order status changes"""
        pass


class CustomerNotificationObserver(OrderObserver):
    """Sends notifications to customers about their order status"""
    
    def __init__(self, notification_method: str = "SMS"):
        self.notification_method = notification_method
        self.notifications_sent = []
    
    def update(self, order: Order, old_status: str, new_status: str):
        """Send notification to customer"""
        message = self._create_message(order, new_status)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        notification = {
            'timestamp': timestamp,
            'order_id': order.order_id,
            'customer': order.customer_name,
            'method': self.notification_method,
            'message': message
        }
        self.notifications_sent.append(notification)
        
        print(f"📱 [{self.notification_method}] to {order.customer_name}: {message}")
    
    def _create_message(self, order: Order, status: str) -> str:
        """Create appropriate message based on status"""
        messages = {
            'confirmed': f"Order #{order.order_id} confirmed! Preparing your food...",
            'preparing': f"Your order #{order.order_id} is being prepared 👨‍🍳",
            'ready': f"Order #{order.order_id} is ready for pickup! 🎉",
            'delivered': f"Order #{order.order_id} has been delivered. Enjoy your meal! 🍔",
            'cancelled': f"Order #{order.order_id} has been cancelled."
        }
        return messages.get(status, f"Order #{order.order_id} status: {status}")


class KitchenDisplayObserver(OrderObserver):
    """Updates kitchen display system with order information"""
    
    def __init__(self):
        self.active_orders = []
    
    def update(self, order: Order, old_status: str, new_status: str):
        """Update kitchen display"""
        if new_status in ['confirmed', 'preparing']:
            if order not in self.active_orders:
                self.active_orders.append(order)
            print(f"🍳 [KITCHEN] Order #{order.order_id} added to queue - {len(order.items)} items")
        elif new_status in ['ready', 'delivered', 'cancelled']:
            if order in self.active_orders:
                self.active_orders.remove(order)
            print(f"🍳 [KITCHEN] Order #{order.order_id} removed from queue")


class AnalyticsObserver(OrderObserver):
    """Collects analytics data from order status changes"""
    
    def __init__(self):
        self.status_changes = []
        self.completed_orders = 0
        self.cancelled_orders = 0
        self.total_revenue = 0.0
    
    def update(self, order: Order, old_status: str, new_status: str):
        """Track analytics"""
        self.status_changes.append({
            'order_id': order.order_id,
            'old_status': old_status,
            'new_status': new_status,
            'timestamp': datetime.now(),
            'total': order.total
        })
        
        if new_status == 'delivered':
            self.completed_orders += 1
            self.total_revenue += order.total
            print(f"📊 [ANALYTICS] Order completed - Total revenue: ${self.total_revenue:.2f}")
        elif new_status == 'cancelled':
            self.cancelled_orders += 1
            print(f"📊 [ANALYTICS] Order cancelled - Total cancellations: {self.cancelled_orders}")
    
    def get_summary(self) -> dict:
        """Get analytics summary"""
        return {
            'total_status_changes': len(self.status_changes),
            'completed_orders': self.completed_orders,
            'cancelled_orders': self.cancelled_orders,
            'total_revenue': self.total_revenue,
            'completion_rate': (self.completed_orders / (self.completed_orders + self.cancelled_orders) * 100) 
                              if (self.completed_orders + self.cancelled_orders) > 0 else 0
        }


class DeliveryCoordinatorObserver(OrderObserver):
    """Coordinates delivery assignments when orders are ready"""
    
    def __init__(self):
        self.pending_deliveries = []
        self.assigned_deliveries = []
    
    def update(self, order: Order, old_status: str, new_status: str):
        """Coordinate delivery"""
        if new_status == 'ready':
            self.pending_deliveries.append(order)
            driver = self._assign_driver(order)
            print(f"🚗 [DELIVERY] Order #{order.order_id} assigned to driver {driver}")
        elif new_status == 'delivered':
            if order in self.pending_deliveries:
                self.pending_deliveries.remove(order)
            self.assigned_deliveries.append(order)
            print(f"🚗 [DELIVERY] Order #{order.order_id} delivery confirmed")
    
    def _assign_driver(self, order: Order) -> str:
        """Simulate driver assignment"""
        drivers = ["Mike", "Sarah", "John", "Emma"]
        import random
        return random.choice(drivers)


class LoyaltyProgramObserver(OrderObserver):
    """Updates customer loyalty points based on orders"""
    
    def __init__(self):
        self.customer_points = {}
    
    def update(self, order: Order, old_status: str, new_status: str):
        """Award loyalty points"""
        if new_status == 'delivered':
            points = int(order.total)  # 1 point per dollar
            customer = order.customer_name
            
            if customer not in self.customer_points:
                self.customer_points[customer] = 0
            
            self.customer_points[customer] += points
            print(f"⭐ [LOYALTY] {customer} earned {points} points! Total: {self.customer_points[customer]}")
    
    def get_customer_points(self, customer_name: str) -> int:
        """Get points for a customer"""
        return self.customer_points.get(customer_name, 0)
