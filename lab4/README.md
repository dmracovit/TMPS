# Restaurant Order System - Behavioral Design Patterns
**Course:** TMPS - Laboratory Work #4  

---

## Objectives

1. Study and understand Behavioral Design Patterns
2. Identify communication patterns between software entities in the system
3. Implement additional functionalities using behavioral design patterns
4. Extend the existing project with at least 1 behavioral pattern

---

## Introduction

Behavioral design patterns are concerned with algorithms and the assignment of responsibilities between objects. These patterns characterize complex control flow that's difficult to follow at runtime and help to identify common communication patterns between objects, thus increasing flexibility in carrying out communication.

This laboratory work extends the Restaurant Order System by implementing behavioral patterns that enhance the communication and interaction between different components of the system.

---

## Domain: Restaurant Order Management System (Extended)

Extension of Labs #2 and #3 with behavioral patterns for:
- Order validation through processing chains
- Event-driven notifications for order status changes
- Dynamic pricing strategy selection

---

## Implemented Design Patterns

### 1. Chain of Responsibility - Order Validation Pipeline

Creates a chain of validators where each validator checks a specific aspect of the order and passes it to the next validator if successful.

```python
# Create validation chain
validator = OrderValidationChain.create_standard_chain()

# Chain automatically processes through all validators
is_valid, message = validator.validate(order)
# Checks: Items → Customer → Amount → Inventory → Business Hours
```

**Validators in Chain:**
- **ItemCountValidator** - Ensures order has at least one item
- **CustomerInfoValidator** - Validates customer name is provided
- **MinimumAmountValidator** - Checks minimum order amount ($5.00)
- **InventoryValidator** - Verifies all items are available
- **BusinessHoursValidator** - Confirms order is within business hours

**Benefits:**
- Decoupled validation logic
- Easy to add/remove validators
- Early termination on first failure
- Flexible chain configuration (standard vs express)

**Location:** `utilities/validation_chain.py`

---

### 2. Observer Pattern - Multi-Channel Notification System

Multiple observers automatically react to order status changes without tight coupling.

```python
# Attach observers to order
order.attach(CustomerNotificationObserver("SMS"))
order.attach(KitchenDisplayObserver())
order.attach(AnalyticsObserver())
order.attach(DeliveryCoordinatorObserver())
order.attach(LoyaltyProgramObserver())

# All observers notified automatically
order.set_status("confirmed")  # Triggers all observers
```

**Implemented Observers:**
- **CustomerNotificationObserver** - Sends SMS/Email notifications to customers
- **KitchenDisplayObserver** - Updates kitchen display with order queue
- **AnalyticsObserver** - Collects metrics and revenue data
- **DeliveryCoordinatorObserver** - Assigns drivers and coordinates delivery
- **LoyaltyProgramObserver** - Awards loyalty points to customers

**Benefits:**
- Loose coupling between order and notification systems
- Easy to add new observers without modifying order class
- Automatic multi-system updates
- Event-driven architecture

**Location:** `utilities/observers.py`

---

### 3. Strategy Pattern - Dynamic Pricing Strategies

Defines a family of pricing algorithms and makes them interchangeable at runtime.

```python
# Create pricing context
pricing = PricingContext()

# Switch strategies at runtime
pricing.set_strategy(HappyHourPricingStrategy(20))  # 20% off
result = pricing.apply_pricing(order)

pricing.set_strategy(BulkOrderStrategy())  # Volume discount
result = pricing.apply_pricing(order)
```

**Pricing Strategies:**
- **RegularPricingStrategy** - Standard pricing with no discounts
- **HappyHourPricingStrategy** - Time-based discounts (14:00-17:00)
- **LoyaltyDiscountStrategy** - Discount based on customer loyalty points
- **BulkOrderStrategy** - Tiered discounts for large orders (5%, 10%, 15%)
- **SeasonalPromotionStrategy** - Special promotional discounts
- **CombinedPricingStrategy** - Applies best available discount

**Benefits:**
- Algorithms encapsulated in separate classes
- Easy to add new pricing strategies
- Runtime strategy selection
- No conditional logic in order processing

**Location:** `utilities/pricing_strategies.py`

---

The client demonstrates:
- **Chain of Responsibility**: Order validation through sequential validators
- **Observer**: Multiple systems reacting to order status changes
- **Strategy**: Different pricing algorithms applied to orders
- **Integration**: All patterns working together in complete order flow

---

## Communication Patterns Implemented

### 1. Sequential Processing (Chain of Responsibility)
Orders flow through validation pipeline where each validator processes and forwards to next.

### 2. Event Broadcasting (Observer)
Order status changes broadcast to multiple independent observers automatically.

### 3. Algorithm Selection (Strategy)
Pricing algorithms selected and swapped at runtime based on business rules.

---

## Key Concepts

**Chain of Responsibility** - Pass request along chain of handlers until one handles it  
**Observer** - Define one-to-many dependency where state changes notify dependents  
**Strategy** - Define family of algorithms and make them interchangeable  

---

## Integration with Previous Labs

**Lab 2 (Creational Patterns):**
- Singleton OrderManager
- Factory Method for menu items
- Builder for complex orders
- Prototype for menu templates

**Lab 3 (Structural Patterns):**
- Decorator for item customization
- Adapter for payment integration
- Facade for simplified workflows
- Proxy for logging/caching

**Lab 4 (Behavioral Patterns):**
- Chain of Responsibility for validation
- Observer for notifications
- Strategy for pricing

All patterns work together to create a flexible, maintainable, and extensible restaurant order management system.

---

## Conclusion

Behavioral patterns enhance the system by:
- **Decoupling** communication between objects
- **Flexibility** in algorithm selection and execution
- **Maintainability** through clear responsibility assignment
- **Extensibility** for adding new behaviors without modifying existing code

The restaurant system now demonstrates 11 design patterns across all three categories (Creational, Structural, and Behavioral), showcasing a comprehensive understanding of object-oriented design principles.
