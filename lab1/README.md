# 🍔 Restaurant Order System

A Python-based restaurant ordering system that demonstrates **SOLID design principles** through a clean, extensible architecture.

## ✨ Features

- **Flexible Discount System**: Support for percentage discounts, fixed amount discounts, and time-based happy hour deals
- **Multiple Payment Methods**: Cash, credit card, and mobile payment options
- **Notification System**: Console and email notifications for order updates
- **Extensible Design**: Easy to add new discount types, payment methods, or notification channels without modifying existing code

## 🎯 SOLID Principles Demonstrated

### **S - Single Responsibility Principle**
Each class has one clear purpose:
- `PercentageDiscount` - handles percentage-based discounts
- `CashPayment` - processes cash transactions
- `EmailNotification` - sends email notifications
- Each component does one thing and does it well!

### **O - Open/Closed Principle**
The system is open for extension but closed for modification:
- Want a new discount type? Create a new class implementing `DiscountStrategy`
- Need cryptocurrency payments? Add a new `PaymentProcessor`
- No need to change existing `OrderProcessor` code!

### **D - Dependency Inversion Principle**
High-level modules depend on abstractions, not concrete implementations:
- `OrderProcessor` works with interfaces (`DiscountStrategy`, `PaymentProcessor`, `NotificationService`)
- Implementations can be swapped easily without touching core logic
- Makes testing and maintenance a breeze!


## 📖 Usage Examples

### Basic Order with Discount
```python
# Create some menu items
burger = MenuItem("Burger", 12.99, "main")
fries = MenuItem("Fries", 4.99, "side")

# Create an order
order = Order(1, [burger, fries])

# Process with 10% discount and cash payment
processor = OrderProcessor(
    discount=PercentageDiscount(10),
    payment=CashPayment(),
    notification=ConsoleNotification()
)
processor.process_order(order)
```

### Happy Hour Special
```python
# Create processor with happy hour discount (5pm-7pm, 25% off)
processor = OrderProcessor(
    discount=HappyHourDiscount(start_hour=17, end_hour=19, percentage=25),
    payment=MobilePayment("+1-555-0123"),
    notification=EmailNotification("customer@example.com")
)
processor.process_order(order)
```

### Credit Card Payment with Fixed Discount
```python
# Process order with $5 off and credit card payment
processor = OrderProcessor(
    discount=FixedAmountDiscount(5),
    payment=CreditCardPayment("1234567890123456"),
    notification=EmailNotification("customer@example.com")
)
processor.process_order(order)
```

## 🏗️ Architecture

### Core Models
- **MenuItem**: Represents items on the restaurant menu
- **Order**: Contains order details, items, and status

### Strategy Patterns (Discounts)
- **NoDiscount**: No discount applied
- **PercentageDiscount**: Percentage-based discounts (e.g., 10% off)
- **FixedAmountDiscount**: Fixed dollar amount off (e.g., $5 off)
- **HappyHourDiscount**: Time-based discounts for happy hour specials

### Payment Processors
- **CashPayment**: Handle cash transactions
- **CreditCardPayment**: Process credit card payments
- **MobilePayment**: Mobile payment processing (Apple Pay, Google Pay, etc.)

### Notification Services
- **ConsoleNotification**: Display notifications in the console
- **EmailNotification**: Send email notifications to customers

### Order Processing
- **OrderProcessor**: Orchestrates the entire order flow using dependency injection
