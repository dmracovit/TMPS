from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

# ============= MODELS =============
class MenuItem:
    """single item from the menu"""
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category
    
    def __str__(self):
        return f"{self.name} (${self.price})"

class Order:
    """customer's order w/ items and status"""
    def __init__(self, order_id: int, items: List[MenuItem]):
        self.order_id = order_id
        self.items = items
        self.timestamp = datetime.utcnow()
        self.status = "pending"
    
    def get_total(self) -> float:
        return sum(item.price for item in self.items)
    
    def __str__(self):
        items_str = ", ".join([item.name for item in self.items])
        return f"Order #{self.order_id}: {items_str} (${self.get_total():.2f})"

# ============= INTERFACES (D - Dependency Inversion) =============
class DiscountStrategy(ABC):
    """interface for discounts"""
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

class PaymentProcessor(ABC):
    """interface for payments"""
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def get_method_name(self) -> str:
        pass

class NotificationService(ABC):
    """interface for notifications"""
    @abstractmethod
    def notify(self, message: str) -> None:
        pass

# ============= DISCOUNT STRATEGIES (S - Single Responsibility & O - Open/Closed) =============
class NoDiscount(DiscountStrategy):
    """no discount, just regular price"""
    def apply_discount(self, total: float) -> float:
        return total
    
    def get_description(self) -> str:
        return "No discount applied"

class PercentageDiscount(DiscountStrategy):
    """handles % based discounts"""
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def apply_discount(self, total: float) -> float:
        return total * (1 - self.percentage / 100)
    
    def get_description(self) -> str:
        return f"{self.percentage}% discount applied"

class FixedAmountDiscount(DiscountStrategy):
    """takes off a fixed dollar amount"""
    def __init__(self, amount: float):
        self.amount = amount
    
    def apply_discount(self, total: float) -> float:
        return max(0, total - self.amount)
    
    def get_description(self) -> str:
        return f"${self.amount} discount applied"

class HappyHourDiscount(DiscountStrategy):
    """time-based discount for happy hours"""
    def __init__(self, start_hour: int, end_hour: int, percentage: float):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.percentage = percentage
    
    def apply_discount(self, total: float) -> float:
        current_hour = datetime.utcnow().hour
        if self.start_hour <= current_hour < self.end_hour:
            return total * (1 - self.percentage / 100)
        return total
    
    def get_description(self) -> str:
        current_hour = datetime.utcnow().hour
        if self.start_hour <= current_hour < self.end_hour:
            return f"Happy Hour {self.percentage}% discount!"
        return "No discount (outside happy hour)"

# ============= PAYMENT PROCESSORS (S - Single Responsibility) =============
class CashPayment(PaymentProcessor):
    """processes cash payments"""
    def process(self, amount: float) -> bool:
        print(f"💵 Received ${amount:.2f} in cash")
        return True
    
    def get_method_name(self) -> str:
        return "Cash"

class CreditCardPayment(PaymentProcessor):
    """processes credit card payments"""
    def __init__(self, card_number: str):
        self.card_number = card_number[-4:]  # last 4 digits only
    
    def process(self, amount: float) -> bool:
        print(f"💳 Charged ${amount:.2f} to card ending in {self.card_number}")
        return True
    
    def get_method_name(self) -> str:
        return f"Credit Card (****{self.card_number})"

class MobilePayment(PaymentProcessor):
    """processes mobile payments (apple pay, google pay, etc)"""
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
    
    def process(self, amount: float) -> bool:
        print(f"📱 Charged ${amount:.2f} via mobile pay to {self.phone_number}")
        return True
    
    def get_method_name(self) -> str:
        return f"Mobile Pay ({self.phone_number})"

# ============= NOTIFICATION SERVICES (S - Single Responsibility) =============
class ConsoleNotification(NotificationService):
    """sends notifications to console"""
    def notify(self, message: str) -> None:
        print(f"🔔 NOTIFICATION: {message}")

class EmailNotification(NotificationService):
    """sends email notifications"""
    def __init__(self, email: str):
        self.email = email
    
    def notify(self, message: str) -> None:
        print(f"📧 Email to {self.email}: {message}")

# ============= ORDER PROCESSOR (O - Open/Closed & D - Dependency Inversion) =============
class OrderProcessor:
    """
    orchestrates the whole order flow
    - depends on interfaces, not concrete implementations (can swap 'em easily)
    - new payment/discount types? just add new classes, don't touch this
    """
    def __init__(self, 
                 discount: DiscountStrategy, 
                 payment: PaymentProcessor,
                 notification: NotificationService):
        self.discount = discount
        self.payment = payment
        self.notification = notification
    
    def process_order(self, order: Order) -> bool:
        print(f"\n{'='*50}")
        print(f"Processing {order}")
        print(f"{'='*50}")
        
        # calc total w/ discount
        original_total = order.get_total()
        final_total = self.discount.apply_discount(original_total)
        
        print(f"Original Total: ${original_total:.2f}")
        print(f"Discount: {self.discount.get_description()}")
        print(f"Final Total: ${final_total:.2f}")
        print(f"Payment Method: {self.payment.get_method_name()}")
        
        # process payment
        if self.payment.process(final_total):
            order.status = "completed"
            self.notification.notify(f"Order #{order.order_id} completed! Total: ${final_total:.2f}")
            return True
        else:
            order.status = "failed"
            self.notification.notify(f"Order #{order.order_id} payment failed!")
            return False

# ============= USAGE EXAMPLES =============
if __name__ == "__main__":
    # create menu items
    burger = MenuItem("Burger", 12.99, "main")
    fries = MenuItem("Fries", 4.99, "side")
    coke = MenuItem("Coke", 2.99, "drink")
    
    # create orders
    order1 = Order(1, [burger, fries, coke])
    order2 = Order(2, [burger, burger, coke])
    
    # example 1: cash payment w/ 10% discount + console notification
    processor1 = OrderProcessor(
        discount=PercentageDiscount(10),
        payment=CashPayment(),
        notification=ConsoleNotification()
    )
    processor1.process_order(order1)
    
    # example 2: credit card w/ $5 off + email notification
    processor2 = OrderProcessor(
        discount=FixedAmountDiscount(5),
        payment=CreditCardPayment("1234567890123456"),
        notification=EmailNotification("customer@example.com")
    )
    processor2.process_order(order2)
    
    # example 3: mobile payment w/ happy hour discount
    processor3 = OrderProcessor(
        discount=HappyHourDiscount(start_hour=17, end_hour=19, percentage=25),
        payment=MobilePayment("+1-555-0123"),
        notification=ConsoleNotification()
    )
    processor3.process_order(order1)
    
    print(f"\n{'='*50}")
    print("✅ 3 SOLID PRINCIPLES DEMONSTRATED:")
    print(f"{'='*50}")
    print("S - Single Responsibility:")
    print("    each class has ONE job (discount, payment, notification)")
    print("\nO - Open/Closed Principle:")
    print("    can add new discount/payment types w/o modifying OrderProcessor")
    print("\nD - Dependency Inversion:")
    print("    OrderProcessor depends on interfaces, not concrete classes")
    print("    easy to swap implementations!")