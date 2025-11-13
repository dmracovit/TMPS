from typing import List, Optional
from models.order import Order
from models.menu_item import MenuItem
from utilities.payment_adapters import PaymentProcessor
from domain.order_manager import OrderManager
from domain.notifications import NotificationService, ConsoleNotification

class OrderProcessingFacade:
    """
    FACADE PATTERN
    Provides a simplified interface to the complex subsystems involved in order processing.
    Hides the complexity of:
    - Order creation and management
    - Payment processing
    - Inventory management
    - Notifications
    - Logging and analytics
    """
    
    def __init__(self):
        self.order_manager = OrderManager()
        self.notification_service: NotificationService = ConsoleNotification()
        self.inventory = InventorySystem()
        self.analytics = AnalyticsSystem()
        self.loyalty_program = LoyaltyProgram()
    
    def create_simple_order(self, customer_name: str, items: List[MenuItem], 
                           payment_processor: PaymentProcessor, 
                           special_instructions: str = "") -> Optional[Order]:
        """
        Simple method that handles the entire order process:
        1. Create order
        2. Check inventory
        3. Process payment
        4. Update inventory
        5. Send notifications
        6. Update analytics
        7. Award loyalty points
        """
        print(f"\n{'='*60}")
        print(f"Processing order for {customer_name}")
        print(f"{'='*60}")
        
        # Step 1: Create order
        order = self.order_manager.create_order()
        order.customer_name = customer_name
        order.special_instructions = special_instructions
        
        for item in items:
            order.add_item(item)
        
        print(f"Order created: {order}")
        
        # Step 2: Check inventory
        if not self.inventory.check_availability(items):
            print("❌ Some items are out of stock!")
            self.notification_service.notify(f"Order #{order.order_id} failed: Items unavailable")
            order.status = "failed"
            return None
        
        # Step 3: Process payment
        total = order.get_total()
        print(f"Total amount: ${total:.2f}")
        
        if not payment_processor.process_payment(total, customer_name):
            print("❌ Payment failed!")
            self.notification_service.notify(f"Order #{order.order_id} payment failed")
            order.status = "failed"
            return None
        
        order.payment_method = payment_processor.get_payment_method_name()
        
        # Step 4: Update inventory
        self.inventory.update_stock(items)
        
        # Step 5: Mark order as completed
        order.status = "completed"
        self.order_manager.complete_order(order.order_id)
        
        # Step 6: Send notifications
        self.notification_service.notify(
            f"Order #{order.order_id} completed for {customer_name}! Total: ${total:.2f}"
        )
        
        # Step 7: Update analytics
        self.analytics.record_sale(order)
        
        # Step 8: Award loyalty points
        points = self.loyalty_program.award_points(customer_name, total)
        print(f"💰 {customer_name} earned {points} loyalty points!")
        
        print(f"✅ Order #{order.order_id} completed successfully!")
        return order
    
    def get_order_status(self, order_id: int) -> Optional[str]:
        """Get order status - simple facade method"""
        order = self.order_manager.get_order(order_id)
        return order.status if order else None
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order - handles all necessary operations"""
        order = self.order_manager.get_order(order_id)
        if not order:
            return False
        
        # Restore inventory
        self.inventory.restore_stock(order.items)
        
        # Update order status
        self.order_manager.cancel_order(order_id)
        
        # Notify customer
        self.notification_service.notify(f"Order #{order_id} has been cancelled")
        
        # Update analytics
        self.analytics.record_cancellation(order)
        
        return True
    
    def get_daily_summary(self) -> dict:
        """Get business analytics summary"""
        return {
            "total_orders": len(self.order_manager.get_all_orders()),
            "completed_orders": len([o for o in self.order_manager.get_all_orders() if o.status == "completed"]),
            "total_revenue": self.order_manager.get_total_revenue(),
            "popular_items": self.analytics.get_popular_items()
        }


# Subsystems that Facade coordinates

class InventorySystem:
    """Manages restaurant inventory"""
    def __init__(self):
        self.stock = {}  # Simplified inventory
    
    def check_availability(self, items: List[MenuItem]) -> bool:
        """Check if all items are in stock"""
        print("Checking inventory...")
        # Simplified - always returns True for demo
        return True
    
    def update_stock(self, items: List[MenuItem]):
        """Update stock after order"""
        print(f"Inventory updated for {len(items)} items")
    
    def restore_stock(self, items: List[MenuItem]):
        """Restore stock after cancellation"""
        print(f"Inventory restored for {len(items)} items")


class AnalyticsSystem:
    """Tracks business analytics"""
    def __init__(self):
        self.sales_data = []
        self.item_frequency = {}
    
    def record_sale(self, order: Order):
        """Record a sale"""
        self.sales_data.append({
            "order_id": order.order_id,
            "amount": order.get_total(),
            "timestamp": order.timestamp
        })
        for item in order.items:
            item_name = item.get_description()
            self.item_frequency[item_name] = self.item_frequency.get(item_name, 0) + 1
        print("📊 Analytics updated")
    
    def record_cancellation(self, order: Order):
        """Record a cancellation"""
        print("📊 Cancellation recorded")
    
    def get_popular_items(self) -> List[str]:
        """Get most popular items"""
        if not self.item_frequency:
            return []
        sorted_items = sorted(self.item_frequency.items(), key=lambda x: x[1], reverse=True)
        return [item[0] for item in sorted_items[:3]]


class LoyaltyProgram:
    """Manages customer loyalty points"""
    def __init__(self):
        self.customer_points = {}
    
    def award_points(self, customer_name: str, order_total: float) -> int:
        """Award points based on order total (1 point per dollar)"""
        points = int(order_total)
        self.customer_points[customer_name] = self.customer_points.get(customer_name, 0) + points
        return points
    
    def get_points(self, customer_name: str) -> int:
        """Get customer's total points"""
        return self.customer_points.get(customer_name, 0)
