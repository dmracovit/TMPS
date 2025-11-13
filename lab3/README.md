# Restaurant Order System - Structural Design Patterns
**Course:** TMPS - Laboratory Work #3

---

## Objectives

1. Study and understand Structural Design Patterns
2. Extend the existing project with structural patterns
3. Implement at least 3 structural design patterns

---

## Domain: Restaurant Order Management System (Extended)

Extension of Lab #2 with structural patterns for enhanced functionality: dynamic item customization, third-party payment integration, simplified order processing, and operation monitoring.

---

## Implemented Design Patterns

### 1. Decorator Pattern - Menu Item Customization

Dynamically adds extras and modifications to menu items without changing base classes.

```python
# Stack decorators to add multiple extras
deluxe_burger = AvocadoDecorator(
    BaconDecorator(
        ExtraCheeseDecorator(burger)
    )
)
# Result: "Burger + Extra Cheese + Bacon + Avocado - $18.49"
```

**Available Decorators:**
- ExtraCheeseDecorator (+$1.50)
- BaconDecorator (+$2.00)
- AvocadoDecorator (+$1.50)
- ExtraSpicyDecorator (+$0.50)
- GlutenFreeDecorator (+$2.00)
- LargeSizeDecorator (+$2.50)

**Location:** `utilities/decorators.py`

---

### 2. Adapter Pattern - Third-Party Payment Integration

Adapts various third-party payment APIs to work with the standard PaymentProcessor interface.

```python
# Integrate different payment services seamlessly
stripe = StripePaymentAdapter("customer@example.com")
paypal = PayPalPaymentAdapter("user@paypal.com")
crypto = CryptoPaymentAdapter("1A2B3C4D5E6F7G8H")

# All use the same interface
stripe.process_payment(25.50, "John Doe")
```

**Adapted Services:**
- Stripe Payment Gateway
- PayPal API
- Cryptocurrency Payments

**Location:** `utilities/payment_adapters.py`

---

### 3. Facade Pattern - Simplified Order Processing

Provides a simple interface to complex subsystems (inventory, payments, notifications, analytics, loyalty).

```python
facade = OrderProcessingFacade()

# Single method handles multiple subsystems
order = facade.create_simple_order(
    customer_name="Alice",
    items=[burger, fries, drink],
    payment_processor=stripe_payment,
    special_instructions="Extra napkins"
)
```

**Coordinated Subsystems:**
- Order Management
- Inventory System
- Payment Processing
- Notification Service
- Analytics System
- Loyalty Program

**Location:** `domain/order_facade.py`

---

### 4. Proxy Pattern - Operation Logging & Caching (Bonus)

Adds logging and caching capabilities to OrderManager transparently.

```python
proxy = OrderManagerProxy()

# Operations are automatically logged and cached
order = proxy.create_order()
proxy.get_order(order.order_id)  # Cached for performance
stats = proxy.get_cache_stats()  # Monitor cache effectiveness
```

**Features:**
- Access logging for all operations
- Order caching for improved performance
- Statistics tracking

**Location:** `utilities/proxy.py`

---


The client demonstrates:
- **Decorator**: Adding extras to menu items
- **Adapter**: Processing payments through different gateways
- **Facade**: Simplifying complex order workflows
- **Proxy**: Logging and caching operations
- **Integration**: All patterns working together

---

## Key Concepts

**Decorator Pattern** - Add responsibilities to objects dynamically  
**Adapter Pattern** - Convert interface of a class into another interface clients expect  
**Facade Pattern** - Provide unified interface to a set of interfaces in a subsystem  
**Proxy Pattern** - Provide surrogate/placeholder for another object to control access  

All patterns enhance the system's flexibility, maintainability, and extensibility while preserving the creational patterns from Lab #2.
